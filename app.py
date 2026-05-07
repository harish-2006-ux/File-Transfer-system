#!/usr/bin/env python3
"""
VaultX - Secure File Transfer System
Clean, deployable version for Render
"""
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, abort
import sqlite3
import os
import bcrypt
import secrets
from datetime import datetime
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import random
import string

# Load environment variables
load_dotenv()

# Configuration
UPLOAD_FOLDER = "server_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size

# Encryption setup
def get_encryption_key():
    key = os.getenv('ENCRYPTION_KEY')
    if not key:
        key = Fernet.generate_key().decode()
        print(f"Generated encryption key: {key}")
    return key.encode() if isinstance(key, str) else key

ENCRYPTION_KEY = get_encryption_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# Database initialization
def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    
    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # File history table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS file_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            filename TEXT NOT NULL,
            action TEXT NOT NULL,
            ip_address TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create test user if not exists
    try:
        test_password = hash_password("Test123!")
        cur.execute("""
            INSERT OR IGNORE INTO users (username, email, password)
            VALUES (?, ?, ?)
        """, ("testuser", "test@example.com", test_password))
        
        # Create your user account
        user_password = hash_password("Test123!")
        cur.execute("""
            INSERT OR IGNORE INTO users (username, email, password)
            VALUES (?, ?, ?)
        """, ("harishvm123", "hhareeshvm@gmail.com", user_password))
    except Exception as e:
        print(f"Error creating test users: {e}")
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_database()

# Utility functions
def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    """Check password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

def generate_otp():
    """Generate 6-digit OTP"""
    return ''.join(random.choices(string.digits, k=6))

def send_otp_email(email, otp):
    """Send OTP via email"""
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    if not sender_email or not sender_password:
        print(f"Email not configured. OTP: {otp}")
        return False
    
    try:
        msg = EmailMessage()
        msg['Subject'] = 'VaultX OTP Verification'
        msg['From'] = sender_email
        msg['To'] = email
        msg.set_content(f'Your VaultX OTP: {otp}\n\nThis code expires in 5 minutes.')
        
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        print(f"OTP sent to {email}")
        return True
    except Exception as e:
        print(f"Email failed: {e}. OTP: {otp}")
        return False

def encrypt_file(input_path, output_path):
    """Encrypt file"""
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
        encrypted = cipher_suite.encrypt(data)
        with open(output_path, 'wb') as f:
            f.write(encrypted)
        return True
    except Exception as e:
        print(f"Encryption error: {e}")
        return False

def decrypt_file(input_path, output_path):
    """Decrypt file"""
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
        decrypted = cipher_suite.decrypt(data)
        with open(output_path, 'wb') as f:
            f.write(decrypted)
        return True
    except Exception as e:
        print(f"Decryption error: {e}")
        return False

def log_file_action(username, filename, action, ip_address):
    """Log file action to database"""
    try:
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO file_history (username, filename, action, ip_address)
            VALUES (?, ?, ?, ?)
        """, (username, filename, action, ip_address))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Logging error: {e}")

# Authentication decorator
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Routes
@app.route('/')
def home():
    """Home page - redirect to dashboard if logged in"""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect("users.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cur.fetchone()
        conn.close()
        
        if user and check_password(password, user[3]):
            # Generate and send OTP
            otp = generate_otp()
            session['pending_username'] = username
            session['pending_otp'] = otp
            session['otp_email'] = user[2]  # email
            
            send_otp_email(user[2], otp)
            flash(f'OTP sent to your email. Check console for OTP: {otp}', 'info')
            return redirect(url_for('verify_otp'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page"""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Basic validation
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('signup.html')
        
        hashed_password = hash_password(password)
        
        try:
            conn = sqlite3.connect("users.db")
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO users (username, email, password)
                VALUES (?, ?, ?)
            """, (username, email, hashed_password))
            conn.commit()
            conn.close()
            
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username or email already exists', 'error')
    
    return render_template('signup.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    """OTP verification page"""
    if 'pending_username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        entered_otp = request.form['otp']
        
        if entered_otp == session.get('pending_otp'):
            # OTP correct - complete login
            session['username'] = session.pop('pending_username')
            session.pop('pending_otp', None)
            session.pop('otp_email', None)
            
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid OTP. Please try again.', 'error')
    
    return render_template('otp_verify.html', email=session.get('otp_email'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    # Get user's files
    files = []
    try:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.startswith(f"{session['username']}_"):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file_size = os.path.getsize(file_path)
                files.append({
                    'name': filename[len(session['username'])+1:],  # Remove username prefix
                    'size': f"{file_size / 1024:.1f} KB",
                    'encrypted_name': filename
                })
    except Exception as e:
        print(f"Error listing files: {e}")
    
    return render_template('dashboard.html', files=files, username=session['username'])

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('dashboard'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('dashboard'))
    
    if file:
        filename = secure_filename(file.filename)
        username = session['username']
        
        # Save original file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{filename}")
        file.save(temp_path)
        
        # Encrypt and save with username prefix
        encrypted_filename = f"{username}_{filename}.enc"
        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename)
        
        if encrypt_file(temp_path, encrypted_path):
            os.remove(temp_path)  # Remove temp file
            log_file_action(username, filename, 'upload', request.remote_addr)
            flash(f'File "{filename}" uploaded and encrypted successfully!', 'success')
        else:
            flash('File encryption failed', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    """Handle file download"""
    username = session['username']
    encrypted_filename = f"{username}_{filename}.enc"
    encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename)
    
    if not os.path.exists(encrypted_path):
        abort(404)
    
    # Decrypt file temporarily
    temp_filename = f"temp_download_{filename}"
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
    
    if decrypt_file(encrypted_path, temp_path):
        log_file_action(username, filename, 'download', request.remote_addr)
        
        def remove_file(response):
            try:
                os.remove(temp_path)
            except:
                pass
            return response
        
        return send_from_directory(
            app.config['UPLOAD_FOLDER'], 
            temp_filename, 
            as_attachment=True, 
            download_name=filename
        )
    else:
        flash('File decryption failed', 'error')
        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'ok', 'service': 'VaultX'}

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error="Server error"), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)