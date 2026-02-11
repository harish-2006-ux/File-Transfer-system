import socket
import os
import hashlib

SERVER_IP = "127.0.0.1"   # change for other PC
PORT = 8080
BUFFER = 1024

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_DIR = os.path.join(BASE_DIR, "client_files")
os.makedirs(CLIENT_DIR, exist_ok=True)

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(BUFFER):
            h.update(chunk)
    return h.hexdigest()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

# ---------- LOGIN ----------
username = input("Username: ")
password = input("Password: ")

client.send(f"{username}|{password}".encode())
response = client.recv(BUFFER).decode()

if response.startswith("AUTH_FAIL"):
    print("Authentication failed")
    client.close()
    exit()

role = response.split("|")[1]
print(f"Login successful ({role})")

# ---------- MENU ----------
while True:
    choice = input("1.Upload  2.Download  3.Exit : ")

    # -------- UPLOAD --------
    if choice == "1":
        filename = input("Enter file name: ")
        path = os.path.join(CLIENT_DIR, filename)

        if not os.path.exists(path):
            print("File not found")
            continue

        client.send(f"UPLOAD {filename}".encode())
        filesize = os.path.getsize(path)
        client.send(str(filesize).encode())

        with open(path, "rb") as f:
            while chunk := f.read(BUFFER):
                client.send(chunk)

        client.send(file_hash(path).encode())
        print(client.recv(BUFFER).decode())

    # -------- DOWNLOAD --------
    elif choice == "2":
        filename = input("Enter file name: ")
        client.send(f"DOWNLOAD {filename}".encode())

        data = client.recv(BUFFER).decode()
        if data == "0":
            print("File not found on server")
            continue
        if data == "PERMISSION_DENIED":
            print("Permission denied")
            continue

        filesize = int(data)
        path = os.path.join(CLIENT_DIR, filename)

        with open(path, "wb") as f:
            received = 0
            while received < filesize:
                chunk = client.recv(BUFFER)
                f.write(chunk)
                received += len(chunk)

        print("File downloaded successfully")

    else:
        break

client.close()
print("Disconnected")
