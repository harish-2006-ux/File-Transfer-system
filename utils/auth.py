"""
Authentication Utilities
Handles password hashing, OTP, and user management
"""

import bcrypt
from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv
import random
from database.supabase_client import create_user as db_create_user, get_user_by_username

load_dotenv()


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        bytes: Hashed password
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def check_password(password: str, hashed: bytes) -> bool:
    """
    Verify a password against its hash
    
    Args:
        password: Plain text password to check
        hashed: Hashed password to compare against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
    except Exception as e:
        print(f"Password check error: {e}")
        return False


def add_user(username: str, email: str, password: str) -> bool:
    """
    Create a new user in the database
    
    Args:
        username: Unique username
        email: User email address
        password: Plain text password
        
    Returns:
        bool: True if user created successfully, False otherwise
    """
    try:
        hashed = hash_password(password)
        result = db_create_user(username, email, hashed.decode('utf-8'))
        return result is not None
    except Exception as e:
        print(f"Error creating user: {e}")
        return False


def get_user(username: str):
    """
    Get user by username
    
    Args:
        username: Username to look up
        
    Returns:
        dict: User data if found, None otherwise
    """
    try:
        return get_user_by_username(username)
    except Exception as e:
        print(f"Error getting user: {e}")
        return None


def send_otp_email(email: str, otp: str) -> bool:
    """
    Send OTP via email
    
    Args:
        email: Recipient email address
        otp: One-time password to send
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Your VaultX OTP'
        msg['From'] = os.getenv('SENDER_EMAIL', 'noreply@vaultx.com')
        msg['To'] = email
        msg.set_content(f'''
Your VaultX One-Time Password (OTP)

Code: {otp}

This code is valid for 5 minutes.
Do not share this code with anyone.

If you didn't request this code, please ignore this email.

---
VaultX Secure File Sharing
        ''')
        
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        
        if not sender_email or not sender_password:
            print("Email credentials not configured")
            return False
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return False


def generate_otp() -> str:
    """
    Generate a random 6-digit OTP
    
    Returns:
        str: 6-digit OTP
    """
    return str(random.randint(100000, 999999))
