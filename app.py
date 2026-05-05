from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory, abort, jsonify
from functools import wraps, lru_cache
import sqlite3
from contextlib import contextmanager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from datetime import datetime
import socket
import psutil
import threading
from auth.utils import hash_password, check_password, add_user, get_user, send_otp_email
from services.encryption import encrypt_file, decrypt_file
from dotenv import load_dotenv
import random
import time
from werkzeug.utils import secure_filename

# Import advanced features (optional - graceful degradation)
try:
    from flask_socketio import SocketIO
    from utils.security import security_monitor, check_password_strength
    from utils.notifications import notification_service
    from utils.websocket_manager import init_websocket_manager, get_websocket_manager
    from utils.analytics import analytics_service
    from utils.search import search_service
    from database.supabase_client import get_supabase, log_file_action, get_user_history
    ADVANCED_FEATURES_ENABLED = True
    print("✅ Advanced features enabled")
except ImportError as e:
    ADVANCED_FEATURES_ENABLED = False
    print(f"⚠️  Advanced features disabled: {e}")
    print("   Run: pip install flask-socketio python-socketio requests")
    security_monitor = None
    notification_service = None
    ws_manager = None
    analytics_service = None
    search_service = None

load_dotenv()

# Configuration
UPLOAD_FOLDER = "server_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'supersecretkeychangeinprod')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Initialize Flask-SocketIO for real-time features (if available)
if ADVANCED_FEATURES_ENABLED:
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
    ws_manager = init_websocket_manager(socketio)
else:
    socketio = None
    ws_manager = None

# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Global state
SERVER_START_TIME = datetime.now()
connection_logs = []
MAX_LOGS = 50
_stats_cache = {}
_stats_lock = threading.Lock()
STATS_CACHE_TTL = 2.0  # Cache stats for 2 seconds

# Database connection pool (thread-local)
_db_pool = threading.local()

def get_db():
    """Get thread-local database connection"""
    if not hasattr(_db_pool, 'conn'):
        _db_pool.conn = sqlite3.connect("users.db", check_same_thread=False)
    return _db_pool.conn

@contextmanager
def get_db_cursor():
    """Context manager for database operations"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        cursor.close()

# Cached network stats
def get_cached_stats():
    """Get cached system stats to reduce CPU overhead"""
    now = time.time()
    with _stats_lock:
        if now - _stats_cache.get('last_update', 0) > STATS_CACHE_TTL:
            net_io = psutil.net_io_counters()
            _stats_cache.update({
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'cpu': psutil.cpu_percent(0.1),
                'memory': psutil.virtual_memory().percent,
                'last_update': now
            })
        return _stats_cache


def add_connection_log(client_ip, method, path, status_code):
    """Add connection log entry (limited to MAX_LOGS)"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {'timestamp': timestamp, 'ip': client_ip, 'method': method, 'path': path, 'status': status_code}
    connection_logs.insert(0, log_entry)
    if len(connection_logs) > MAX_LOGS:
        connection_logs.pop()

def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            flash('Please log in first.')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

def init_dbs():
    """Initialize SQLite databases"""
    # Users database
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

    # Transfers database
    conn = sqlite3.connect("transfers.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            filename TEXT,
            action TEXT NOT NULL,
            ip TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_dbs()

def log_action(username, filename, action):
    """Log user action to database"""
    ip = request.remote_addr if request else 'unknown'
    conn = sqlite3.connect("transfers.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (username, filename, action, ip, timestamp) VALUES (?, ?, ?, ?, ?)",
        (username or 'anonymous', filename or '-', action, ip, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

# Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    """User login with OTP verification and suspicious activity detection"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        
        user = get_user(username)
        
        if user and check_password(password, user[3]):
            # Get user's last login info
            user_email = user[2]
            last_ip = session.get(f'{username}_last_ip')
            last_user_agent = session.get(f'{username}_last_user_agent')
            
            # Check for suspicious login (if advanced features enabled)
            is_suspicious = False
            reasons = []
            location = {}
            
            if ADVANCED_FEATURES_ENABLED and security_monitor:
                is_suspicious, reasons = security_monitor.is_suspicious_login(
                    username, ip, last_ip, user_agent, last_user_agent
                )
                location = security_monitor.get_geolocation(ip)
                
                # Log security event
                if is_suspicious:
                    security_monitor.log_security_event(
                        username, 'SUSPICIOUS_LOGIN', ip,
                        {'reasons': reasons, 'location': location}
                    )
                    
                    # Send suspicious login alert
                    if notification_service:
                        notification_service.send_suspicious_login_alert(
                            user_email, username, ip, reasons
                        )
                
                # Clear failed attempts on successful login
                security_monitor.clear_failed_attempts(ip)
            
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            session['temp_user'] = username
            session['temp_user_email'] = user_email
            session['otp'] = otp
            session['temp_ip'] = ip
            session['temp_user_agent'] = user_agent
            session['temp_location'] = location
            session['is_suspicious'] = is_suspicious
            session.permanent = True
            
            # Always print OTP to console for development
            print("=" * 60)
            print(f"🔐 OTP for {username}: {otp}")
            print("=" * 60)
            
            # Send OTP via email
            email_sent = send_otp_email(user_email, otp)
            if email_sent:
                flash('OTP sent to your email. Check inbox/spam.')
            else:
                flash(f'OTP: {otp} (Email not configured - check terminal)')
            
            return redirect('/otp_verify')
        else:
            # Record failed attempt (if advanced features enabled)
            if ADVANCED_FEATURES_ENABLED and security_monitor:
                security_monitor.record_failed_attempt(ip)
                security_monitor.log_security_event(
                    username or 'unknown', 'FAILED_LOGIN', ip,
                    {'reason': 'Invalid credentials'}
                )
                
                # Check if IP is locked out
                if security_monitor.is_ip_locked_out(ip):
                    flash('Too many failed attempts. Please try again later.')
                else:
                    flash('Invalid username or password.')
            else:
                flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
@limiter.limit("3 per minute")
def signup():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not username or not email or not password:
            flash('All fields are required.')
            return render_template('signup.html')
        
        if add_user(username, email, password):
            flash('Account created successfully! Please login.')
            return redirect('/login')
        else:
            flash('Username already exists.')
    
    return render_template('signup.html')

@app.route('/otp_verify', methods=['GET', 'POST'])
def otp_verify():
    """Verify OTP for login"""
    if 'otp' not in session or 'temp_user' not in session:
        flash("Session expired. Please login again.")
        return redirect('/login')
    
    if request.method == 'POST':
        entered_otp = request.form.get('otp', '').strip()
        
        if entered_otp == str(session['otp']):
            # OTP verified - complete login
            username = session['temp_user']
            user_email = session.get('temp_user_email')
            ip = session.get('temp_ip', request.remote_addr)
            user_agent = session.get('temp_user_agent', '')
            location = session.get('temp_location', {})
            is_suspicious = session.get('is_suspicious', False)
            
            # Set user session
            session['user'] = username
            session[f'{username}_last_ip'] = ip
            session[f'{username}_last_user_agent'] = user_agent
            
            # Clean up temp session data
            session.pop('otp', None)
            session.pop('temp_user', None)
            session.pop('temp_user_email', None)
            session.pop('temp_ip', None)
            session.pop('temp_user_agent', None)
            session.pop('temp_location', None)
            session.pop('is_suspicious', None)
            
            # Log action
            log_action(username, None, 'LOGIN')
            
            # Send login notification (only if not suspicious and advanced features enabled)
            if ADVANCED_FEATURES_ENABLED and not is_suspicious and user_email and notification_service:
                notification_service.send_login_notification(
                    user_email, username, ip, location,
                    user_agent[:50]  # Truncate user agent
                )
            
            # WebSocket notification (if available)
            if ws_manager:
                ws_manager.notify_login(username, ip, location)
            
            flash('Login successful!')
            return redirect('/')
        else:
            flash('Invalid OTP. Please try again.')
    
    return render_template('otp_verify.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    username = session.pop('user', None)
    log_action(username, None, 'LOGOUT')
    flash('Logged out successfully.')
    return redirect('/login')

# File Management Routes
@app.route("/")
@login_required
def home():
    """Dashboard - file list and recent activity"""
    add_connection_log(request.remote_addr, "GET", "/", 200)
    username = session['user']
    
    # Get encrypted files
    files = [f[:-4] for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.enc')]
    
    # Get recent history
    conn = sqlite3.connect("transfers.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT filename, action, timestamp FROM history WHERE username = ? ORDER BY id DESC LIMIT 5",
        (username,)
    )
    history = cur.fetchall()
    conn.close()
    
    return render_template("home.html", files=files, history=history, session=session)

@app.route("/upload", methods=["POST"])
@login_required
@limiter.limit("10 per minute")
def upload():
    """Upload and encrypt file"""
    if 'file' not in request.files:
        flash('No file selected.')
        return redirect('/')
    
    file = request.files['file']
    if not file or not file.filename:
        flash('No file selected.')
        return redirect('/')
    
    filename = secure_filename(file.filename)
    temp_path = os.path.join(UPLOAD_FOLDER, filename)
    enc_path = os.path.join(UPLOAD_FOLDER, filename + '.enc')
    
    try:
        # Save and encrypt
        file.save(temp_path)
        file_size = os.path.getsize(temp_path)
        file_size_str = f"{file_size / 1024:.2f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.2f} MB"
        
        encrypt_file(temp_path, enc_path)
        os.remove(temp_path)
        
        username = session['user']
        log_action(username, filename, 'UPLOAD')
        
        # Get user email for notification (if advanced features enabled)
        if ADVANCED_FEATURES_ENABLED:
            user = get_user(username)
            if user:
                user_email = user[2]
                
                # Send email notification
                if notification_service:
                    notification_service.send_file_upload_notification(
                        user_email, username, filename, file_size_str
                    )
        
        # WebSocket notification (if available)
        if ws_manager:
            ws_manager.notify_file_upload(username, filename, file_size_str)
        
        flash(f'File "{filename}" uploaded and encrypted successfully!')
    except Exception as e:
        flash(f'Upload failed: {str(e)}')
    
    return redirect('/')

@app.route("/download/<filename>")
@login_required
def download(filename):
    """Decrypt and download file"""
    enc_path = os.path.join(UPLOAD_FOLDER, filename + '.enc')
    
    if not os.path.exists(enc_path):
        abort(404)
    
    temp_path = os.path.join(UPLOAD_FOLDER, filename)
    
    try:
        # Decrypt temporarily
        decrypt_file(enc_path, temp_path)
        username = session['user']
        log_action(username, filename, 'DOWNLOAD')
        
        # WebSocket notification
        if ws_manager:
            ws_manager.notify_file_download(username, filename)
        
        # Send file and cleanup
        response = send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
        
        # Schedule cleanup after response
        @response.call_on_close
        def cleanup():
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        return response
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        flash(f'Download failed: {str(e)}')
        return redirect('/')

@app.route("/delete/<filename>")
@login_required
def delete(filename):
    """Delete encrypted file"""
    enc_path = os.path.join(UPLOAD_FOLDER, filename + '.enc')
    
    if os.path.exists(enc_path):
        try:
            os.remove(enc_path)
            username = session['user']
            log_action(username, filename, 'DELETE')
            
            # WebSocket notification
            if ws_manager:
                ws_manager.notify_file_delete(username, filename)
            
            flash(f'File "{filename}" deleted successfully!')
        except Exception as e:
            flash(f'Delete failed: {str(e)}')
    else:
        flash('File not found.')
    
    return redirect('/')

@app.route("/share/<filename>", methods=["POST"])
@login_required
@limiter.limit("5 per minute")
def share_file(filename):
    """Share file via email"""
    recipient_email = request.form.get('email', '').strip()
    
    if not recipient_email:
        flash('Please enter an email address.')
        return redirect('/')
    
    # Basic email validation
    if '@' not in recipient_email or '.' not in recipient_email:
        flash('Please enter a valid email address.')
        return redirect('/')
    
    enc_path = os.path.join(UPLOAD_FOLDER, filename + '.enc')
    
    if not os.path.exists(enc_path):
        flash('File not found.')
        return redirect('/')
    
    username = session['user']
    
    # Get file size
    file_size = os.path.getsize(enc_path)
    file_size_str = f"{file_size / 1024:.2f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.2f} MB"
    
    # Send email notification
    try:
        from email.message import EmailMessage
        import smtplib
        
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        
        if not sender_email or not sender_password:
            flash('Email not configured. Please set SENDER_EMAIL and SENDER_PASSWORD in .env')
            return redirect('/')
        
        msg = EmailMessage()
        msg['Subject'] = f'🔐 {username} shared "{filename}" with you on VaultX'
        msg['From'] = sender_email
        msg['To'] = recipient_email
        
        # Create HTML email
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h1 style="color: white; margin: 0;">📁 File Shared with You</h1>
                </div>
                
                <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #667eea;">VaultX File Share</h2>
                    
                    <p><strong>{username}</strong> has shared a file with you on VaultX!</p>
                    
                    <div style="background: #f0f4ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 5px 0;"><strong>📄 Filename:</strong> {filename}</p>
                        <p style="margin: 5px 0;"><strong>📊 Size:</strong> {file_size_str}</p>
                        <p style="margin: 5px 0;"><strong>👤 Shared by:</strong> {username}</p>
                        <p style="margin: 5px 0;"><strong>🔐 Status:</strong> <span style="color: #28a745;">Encrypted & Secure</span></p>
                    </div>
                    
                    <div style="background: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0;">
                        <p style="margin: 0;">✅ This file is protected with AES-256 encryption</p>
                    </div>
                    
                    <p><strong>To access this file:</strong></p>
                    <ol style="line-height: 2;">
                        <li>Create an account on VaultX if you don't have one</li>
                        <li>Contact {username} for access instructions</li>
                        <li>Login to VaultX to download the file</li>
                    </ol>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://127.0.0.1:8000/" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            Go to VaultX
                        </a>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    
                    <p style="font-size: 12px; color: #666;">
                        This is an automated notification from VaultX.<br>
                        VaultX - Secure File Sharing System
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.set_content(f"""
VaultX File Share

{username} has shared a file with you on VaultX!

Filename: {filename}
Size: {file_size_str}
Shared by: {username}
Status: Encrypted & Secure

To access this file:
1. Create an account on VaultX if you don't have one
2. Contact {username} for access instructions
3. Login to VaultX to download the file

Go to VaultX: http://127.0.0.1:8000/

---
This is an automated notification from VaultX.
VaultX - Secure File Sharing System
        """)
        msg.add_alternative(html_content, subtype='html')
        
        # Send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        
        # Log the share action
        log_action(username, filename, 'SHARE')
        
        print(f"✅ File '{filename}' shared with {recipient_email} by {username}")
        flash(f'File "{filename}" shared with {recipient_email} successfully!')
        
    except Exception as e:
        print(f"❌ Error sharing file: {e}")
        flash(f'Failed to share file: {str(e)}')
    
    return redirect('/')

@app.route("/profile")
@login_required
def profile():
    """User profile with activity history"""
    username = session['user']
    
    conn = sqlite3.connect("transfers.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT filename, action, ip, timestamp FROM history WHERE username = ? ORDER BY id DESC LIMIT 20",
        (username,)
    )
    history = cur.fetchall()
    conn.close()
    
    return render_template("profile.html", history=history, username=username)

# Network Monitoring Routes
@app.route("/network")
@login_required
def network_status():
    """Network and system status dashboard"""
    add_connection_log(request.remote_addr, "GET", "/network", 200)
    
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    uptime = datetime.now() - SERVER_START_TIME
    uptime_str = str(uptime).split('.')[0]
    
    stats = get_cached_stats()
    total_files = len([f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.enc')])
    
    info = {
        'hostname': hostname,
        'local_ip': local_ip,
        'port': 8000,
        'uptime': uptime_str,
        'total_bytes_sent': stats['bytes_sent'],
        'total_bytes_recv': stats['bytes_recv'],
        'total_files': total_files,
        'memory_percent': round(stats['memory'], 1),
        'cpu_percent': round(stats['cpu'], 1),
        'status': 'Online'
    }
    
    return render_template("network.html", network=info, logs=connection_logs[:20])

@app.route("/network-stats")
def network_stats():
    """API endpoint for real-time network stats"""
    stats = get_cached_stats()
    return jsonify({
        "sent": round(stats['bytes_sent'] / 1024 / 1024, 2),  # MB
        "received": round(stats['bytes_recv'] / 1024 / 1024, 2),  # MB
        "cpu": stats['cpu'],
        "memory": stats['memory']
    })

# ============================================================
# ANALYTICS ROUTES
# ============================================================

@app.route("/analytics")
@login_required
def analytics_dashboard():
    """Analytics dashboard with charts and statistics"""
    username = session['user']
    
    # Get statistics
    user_stats = analytics_service.get_user_statistics(username, days=30)
    security_insights = analytics_service.get_security_insights(username, days=30)
    
    return render_template(
        "analytics.html",
        stats=user_stats,
        security=security_insights,
        username=username
    )

@app.route("/api/analytics/chart/<chart_type>")
@login_required
def get_chart_data(chart_type):
    """API endpoint for chart data"""
    username = session['user']
    days = request.args.get('days', 30, type=int)
    
    chart_data = analytics_service.get_chart_data(username, chart_type, days)
    return jsonify(chart_data)

@app.route("/api/analytics/report")
@login_required
def generate_analytics_report():
    """Generate analytics report"""
    username = session['user']
    report_type = request.args.get('type', 'summary')
    
    report = analytics_service.generate_report(username, report_type)
    return jsonify(report)

# ============================================================
# SEARCH ROUTES
# ============================================================

@app.route("/search")
@login_required
def search_page():
    """Advanced search page"""
    return render_template("search.html", username=session['user'])

@app.route("/api/search")
@login_required
def api_search():
    """API endpoint for search"""
    username = session['user']
    query = request.args.get('q', '')
    search_type = request.args.get('type', 'files')
    
    if search_type == 'files':
        results = search_service.search_files(username, query)
    elif search_type == 'activity':
        results = search_service.search_activity(username, query)
    elif search_type == 'security':
        results = search_service.search_security_events(username, query)
    else:
        results = []
    
    return jsonify({'results': results, 'count': len(results)})

@app.route("/api/search/advanced", methods=['POST'])
@login_required
def api_advanced_search():
    """API endpoint for advanced search"""
    username = session['user']
    search_params = request.json
    
    results = search_service.advanced_search(username, search_params)
    return jsonify(results)

@app.route("/api/search/suggestions")
@login_required
def api_search_suggestions():
    """API endpoint for search suggestions"""
    username = session['user']
    partial_query = request.args.get('q', '')
    
    suggestions = search_service.get_search_suggestions(username, partial_query)
    return jsonify({'suggestions': suggestions})

# ============================================================
# SECURITY ROUTES
# ============================================================

@app.route("/security")
@login_required
def security_dashboard():
    """Security dashboard"""
    username = session['user']
    
    # Get security insights
    insights = analytics_service.get_security_insights(username, days=30)
    
    # Get recent security events
    events = security_monitor.get_security_events(username, limit=50)
    
    return render_template(
        "security.html",
        insights=insights,
        events=events,
        username=username
    )

@app.route("/api/security/events")
@login_required
def api_security_events():
    """API endpoint for security events"""
    username = session['user']
    limit = request.args.get('limit', 50, type=int)
    
    events = security_monitor.get_security_events(username, limit)
    return jsonify({'events': events, 'count': len(events)})

# ============================================================
# WEBSOCKET EVENTS
# ============================================================

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    if 'user' in session:
        username = session['user']
        print(f"WebSocket: User {username} connected")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    if 'user' in session:
        username = session['user']
        print(f"WebSocket: User {username} disconnected")

@socketio.on('join_room')
def handle_join_room(data):
    """Handle user joining their room"""
    if 'user' in session:
        username = session['user']
        if ws_manager:
            # User joins their personal room for notifications
            from flask_socketio import join_room
            join_room(f"user_{username}")
            print(f"WebSocket: User {username} joined room")

@socketio.on('request_stats')
def handle_stats_request():
    """Handle request for real-time stats"""
    stats = get_cached_stats()
    if ws_manager:
        ws_manager.broadcast_system_stats({
            'cpu': stats['cpu'],
            'memory': stats['memory'],
            'bytes_sent': stats['bytes_sent'],
            'bytes_recv': stats['bytes_recv']
        })

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return render_template('login.html'), 404

@app.errorhandler(500)
def server_error(e):
    return "Internal server error", 500

if __name__ == '__main__':
    print("=" * 60)
    print("VaultX - Secure File Sharing System")
    print("=" * 60)
    print(f"Server starting on http://127.0.0.1:8000")
    print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print("=" * 60)
    
    if ADVANCED_FEATURES_ENABLED:
        print("🔐 Advanced Features Enabled:")
        print("  ✅ Suspicious Login Detection")
        print("  ✅ Email Notifications")
        print("  ✅ Real-time WebSocket Updates")
        print("  ✅ Analytics Dashboard")
        print("  ✅ Advanced Search System")
        print("  ✅ Security Monitoring")
    else:
        print("⚠️  Running in Basic Mode")
        print("   To enable advanced features, install:")
        print("   pip install flask-socketio python-socketio requests")
    
    print("=" * 60)
    
    # Use socketio.run if available, otherwise regular Flask
    if socketio:
        socketio.run(app, host="127.0.0.1", port=8000, debug=True, allow_unsafe_werkzeug=True)
    else:
        app.run(host="127.0.0.1", port=8000, debug=True)
