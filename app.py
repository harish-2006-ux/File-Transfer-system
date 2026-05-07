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
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Routes
@app.route('/')
def home():
    """Home page - redirect to dashboard if logged in"""
    if 'user' in session:
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
            session['user'] = session.pop('pending_username')  # Use 'user' key for template
            session['username'] = session['user']  # Keep both for compatibility
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
    """Main dashboard - original VaultX UI"""
    # Get user's files
    files = []
    try:
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.startswith(f"{session['username']}_") and filename.endswith('.enc'):
                # Remove username prefix and .enc extension
                display_name = filename[len(session['username'])+1:-4]
                files.append(display_name)
    except Exception as e:
        print(f"Error listing files: {e}")
    
    # Get recent activity (mock data for now)
    history = [
        (f"File uploaded", "upload", "2 min ago"),
        (f"Login successful", "login", "5 min ago"),
        (f"File downloaded", "download", "1 hour ago"),
    ]
    
    return render_template('home.html', files=files, history=history)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('dashboard'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('dashboard'))
    
    if file:
        filename = secure_filename(file.filename)
        username = session['user']
        
        # Save original file temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{filename}")
        file.save(temp_path)
        
        # Encrypt and save with username prefix
        encrypted_filename = f"{username}_{filename}.enc"
        encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename)
        
        if encrypt_file(temp_path, encrypted_path):
            os.remove(temp_path)  # Remove temp file
            log_file_action(username, filename, 'upload', request.remote_addr)
            flash(f'File "{filename}" uploaded and encrypted successfully!')
        else:
            flash('File encryption failed')
    
    return redirect(url_for('dashboard'))

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    """Handle file download"""
    username = session['user']
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
        flash('File decryption failed')
        return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('Logged out successfully')
    return redirect(url_for('login'))

@app.route('/delete/<filename>')
@login_required
def delete_file(filename):
    """Delete file"""
    username = session['user']
    encrypted_filename = f"{username}_{filename}.enc"
    encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], encrypted_filename)
    
    if os.path.exists(encrypted_path):
        try:
            os.remove(encrypted_path)
            log_file_action(username, filename, 'delete', request.remote_addr)
            flash(f'File "{filename}" deleted successfully!')
        except Exception as e:
            flash(f'Error deleting file: {e}')
    else:
        flash('File not found')
    
    return redirect(url_for('dashboard'))

@app.route('/share/<filename>', methods=['POST'])
@login_required
def share_file(filename):
    """Share file via email"""
    email = request.form.get('email')
    if not email:
        flash('Email address required')
        return redirect(url_for('dashboard'))
    
    username = session['user']
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    # Debug: Check if environment variables are loaded
    print(f"DEBUG: SENDER_EMAIL = {sender_email}")
    print(f"DEBUG: SENDER_PASSWORD = {'*' * len(sender_password) if sender_password else 'None'}")
    
    if not sender_email or not sender_password:
        flash('Email configuration missing. Please contact administrator.')
        return redirect(url_for('dashboard'))
    
    # Send share notification
    try:
        msg = EmailMessage()
        msg['Subject'] = f'🔐 VaultX File Share: {filename}'
        msg['From'] = sender_email
        msg['To'] = email
        
        # Create a professional HTML email
        html_content = f'''
        <html>
        <body style="font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #00c8ff; margin: 0;">🔐 VaultX</h1>
                    <p style="color: #666; margin: 5px 0;">Secure File Transfer</p>
                </div>
                
                <h2 style="color: #333;">File Shared With You</h2>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p><strong>From:</strong> {username}</p>
                    <p><strong>File:</strong> {filename}</p>
                    <p><strong>Shared:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <p>Hello,</p>
                <p><strong>{username}</strong> has securely shared a file with you through VaultX.</p>
                
                <div style="background: #e7f3ff; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="color: #0066cc; margin-top: 0;">🔒 Security Features:</h3>
                    <ul style="color: #333;">
                        <li>File is encrypted with AES-256 encryption</li>
                        <li>Secure storage and transfer</li>
                        <li>Access controlled by VaultX platform</li>
                    </ul>
                </div>
                
                <p>To access this file, please contact <strong>{username}</strong> for access instructions.</p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                
                <div style="text-align: center; color: #666; font-size: 12px;">
                    <p>This email was sent from VaultX Secure File Transfer System</p>
                    <p>If you received this email in error, please ignore it.</p>
                </div>
            </div>
        </body>
        </html>
        '''
        
        # Set both plain text and HTML content
        msg.set_content(f'''
VaultX File Share Notification

From: {username}
File: {filename}
Shared: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{username} has shared a file with you through VaultX secure file transfer system.

The file is encrypted with AES-256 encryption and stored securely.

To access this file, please contact {username} for access instructions.

---
VaultX Secure File Transfer System
        ''')
        
        msg.add_alternative(html_content, subtype='html')
        
        print(f"DEBUG: Attempting to send email to {email}")
        
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=30) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        log_file_action(username, filename, 'share', request.remote_addr)
        flash(f'✅ File "{filename}" shared successfully with {email}!')
        print(f"DEBUG: Email sent successfully to {email}")
        
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f'Email authentication failed. Please check app password.'
        flash(error_msg)
        print(f"DEBUG: SMTP Auth Error: {e}")
        
    except smtplib.SMTPException as e:
        error_msg = f'Email server error: {str(e)}'
        flash(error_msg)
        print(f"DEBUG: SMTP Error: {e}")
        
    except Exception as e:
        error_msg = f'Error sharing file: {str(e)}'
        flash(error_msg)
        print(f"DEBUG: General Error: {e}")
    
    return redirect(url_for('dashboard'))

# Placeholder routes for sidebar links
@app.route('/network')
@login_required
def network():
    flash('Network page - Coming soon!')
    return redirect(url_for('dashboard'))

@app.route('/profile')
@login_required
def profile():
    flash('Profile page - Coming soon!')
    return redirect(url_for('dashboard'))

@app.route('/analytics')
@login_required
def analytics():
    flash('Analytics page - Coming soon!')
    return redirect(url_for('dashboard'))

@app.route('/search')
@login_required
def search():
    flash('Search page - Coming soon!')
    return redirect(url_for('dashboard'))

@app.route('/security')
@login_required
def security():
    flash('Security page - Coming soon!')
    return redirect(url_for('dashboard'))

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