import socket
import os
import hashlib
import concurrent.futures

HOST = "0.0.0.0"
PORT = 8080
BUFFER = 1024
NUM_WORKERS = int(os.getenv("NUM_WORKERS", "4"))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_DIR = os.path.join(BASE_DIR, "server_files")
USER_FILE = os.path.join(BASE_DIR, "users.txt")

os.makedirs(SERVER_DIR, exist_ok=True)

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def authenticate(username, password):
    if not os.path.exists(USER_FILE):
        return None

    hashed = hash_password(password)
    with open(USER_FILE, "r") as f:
        for line in f:
            user, pwd, role = line.strip().split(":")
            if user == username and pwd == hashed:
                return role
    return None

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(BUFFER):
            h.update(chunk)
    return h.hexdigest()

def handle_client(conn, addr):
    # ---------- AUTHENTICATION ----------
    auth_data = conn.recv(BUFFER).decode()
    username, password = auth_data.split("|")

    role = authenticate(username, password)
    if not role:
        conn.send(b"AUTH_FAIL")
        conn.close()
        return

    conn.send(f"AUTH_SUCCESS|{role}".encode())
    print(f"User authenticated: {username} ({role})")

    # ---------- COMMAND HANDLING ----------
    while True:
        cmd_data = conn.recv(BUFFER).decode()
        if not cmd_data:
            break

        parts = cmd_data.split()
        command = parts[0]

        # -------- UPLOAD --------
        if command == "UPLOAD":
            if role != "admin":
                conn.send(b"PERMISSION_DENIED")
                continue

            filename = parts[1]
            filepath = os.path.join(SERVER_DIR, filename)

            filesize = int(conn.recv(BUFFER).decode())
            with open(filepath, "wb") as f:
                received = 0
                while received < filesize:
                    data = conn.recv(BUFFER)
                    f.write(data)
                    received += len(data)

            client_hash = conn.recv(BUFFER).decode()
            server_hash = file_hash(filepath)

            if client_hash == server_hash:
                conn.send(b"UPLOAD_SUCCESS_INTEGRITY_OK")
                print(f"{username} uploaded {filename} (verified)")
            else:
                conn.send(b"UPLOAD_FAILED_CORRUPTED")

        # -------- DOWNLOAD --------
        elif command == "DOWNLOAD":
            if role not in ["admin", "user"]:
                conn.send(b"PERMISSION_DENIED")
                continue

            filename = parts[1]
            filepath = os.path.join(SERVER_DIR, filename)

            if not os.path.exists(filepath):
                conn.send(b"0")
                continue

            filesize = os.path.getsize(filepath)
            conn.send(str(filesize).encode())

            with open(filepath, "rb") as f:
                while chunk := f.read(BUFFER):
                    conn.send(chunk)

            print(f"{username} downloaded {filename}")

    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)  # Allow multiple pending connections

print(f"Secure FTP Server running on {HOST}:{PORT} with {NUM_WORKERS} workers...")

with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
    try:
        while True:
            conn, addr = server.accept()
            print(f"Client connected: {addr}")
            executor.submit(handle_client, conn, addr)
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server.close()
        print("Server stopped.")
