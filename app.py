from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
import sqlite3
import hashlib
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secureftpkey"

UPLOAD_FOLDER = "server_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =============================
# EMAIL CONFIGURATION
# =============================
SENDER_EMAIL = "hhareeshvm@gmail.com"
SENDER_PASSWORD = "iyro tjyi jmfd niis"

# =============================
# DATABASE INIT
# =============================
def init_users_db():
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def init_transfer_db():
    conn = sqlite3.connect("transfers.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            filename TEXT,
            action TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

init_users_db()
init_transfer_db()

# =============================
# HELPERS
# =============================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def log_action(user, filename, action):
    conn = sqlite3.connect("transfers.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history VALUES (NULL,?,?,?,?)",
        (user, filename, action, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def send_file_email(receiver_email, filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    msg = EmailMessage()
    msg["Subject"] = "File Shared From Secure FTP"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email

    msg.set_content(f"""
Hello,

A file has been shared with you.

File Name: {filename}

Regards,
Secure FTP System
""")

    # Attach file
    with open(file_path, "rb") as f:
        file_data = f.read()
        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="octet-stream",
            filename=filename
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

# =============================
# ROUTES
# =============================

@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    files = os.listdir(UPLOAD_FOLDER)

    conn = sqlite3.connect("transfers.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT filename, action FROM history WHERE username=? ORDER BY id DESC LIMIT 5",
        (session["user"],)
    )
    history = cur.fetchall()
    conn.close()

    return render_template("home.html", files=files, history=history)

# =============================
# CREATE FILE
# =============================
@app.route("/create-file", methods=["POST"])
def create_file():
    if "user" not in session:
        return redirect(url_for("login"))

    filename = request.form["filename"]

    if filename:
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "w") as f:
            f.write("")

        log_action(session["user"], filename, "CREATE")
        flash("File created successfully!")

    return redirect(url_for("home"))

# =============================
# UPLOAD FILE
# =============================
@app.route("/upload", methods=["POST"])
def upload():
    if "user" not in session:
        return redirect(url_for("login"))

    file = request.files["file"]

    if file and file.filename:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        log_action(session["user"], file.filename, "UPLOAD")
        flash("File uploaded successfully!")

    return redirect(url_for("home"))

# =============================
# DOWNLOAD FILE
# =============================
@app.route("/download/<filename>")
def download(filename):
    if "user" not in session:
        return redirect(url_for("login"))

    log_action(session["user"], filename, "DOWNLOAD")
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# =============================
# DELETE FILE
# =============================
@app.route("/delete/<filename>")
def delete(filename):
    if "user" not in session:
        return redirect(url_for("login"))

    os.remove(os.path.join(UPLOAD_FOLDER, filename))
    log_action(session["user"], filename, "DELETE")
    flash("File deleted successfully!")

    return redirect(url_for("home"))

# =============================
# SHARE FILE (REAL EMAIL)
# =============================
@app.route("/share/<filename>", methods=["POST"])
def share_file(filename):
    if "user" not in session:
        return redirect(url_for("login"))

    receiver_email = request.form["email"]

    try:
        send_file_email(receiver_email, filename)
        log_action(session["user"], filename, f"SHARED to {receiver_email}")
        flash("File shared successfully!")
    except Exception as e:
        flash("Error sending email. Check credentials.")

    return redirect(url_for("home"))

# =============================
# AUTH ROUTES
# =============================

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            conn = sqlite3.connect("users.db")
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users VALUES (NULL,?,?,?)",
                (
                    request.form["username"],
                    request.form["email"],
                    hash_password(request.form["password"])
                )
            )
            conn.commit()
            conn.close()
            flash("Account created! Please login.")
            return redirect(url_for("login"))
        except:
            flash("Username already exists!")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (
                request.form["username"],
                hash_password(request.form["password"])
            )
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password")

    return render_template("login.html")

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("transfers.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT filename, action, timestamp FROM history WHERE username=? ORDER BY id DESC LIMIT 10",
        (session["user"],)
    )
    history = cur.fetchall()
    conn.close()

    return render_template("profile.html", history=history)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# =============================
# RUN APP
# =============================
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)

