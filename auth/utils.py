import bcrypt
import sqlite3
from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv
import pyotp
import random

load_dotenv()

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def add_user(username: str, email: str, password: str) -> bool:
    hashed = hash_password(password)
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        cur.close()
        conn.close()

def get_user(username: str):
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def send_otp_email(email: str, otp: str) -> bool:
    msg = EmailMessage()
    msg['Subject'] = 'Your VaultX OTP'
    msg['From'] = os.getenv('SENDER_EMAIL')
    msg['To'] = email
    msg.set_content(f'Your OTP: {otp} (5min valid)')
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.getenv('SENDER_EMAIL'), os.getenv('SENDER_PASSWORD'))
            server.send_message(msg)
        return True
    except:
        return False

def generate_totp_secret() -> str:
    return pyotp.random_base32()

def verify_totp(user_otp: str, secret: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(user_otp)
