# 🚀 VaultX Quick Start Guide

Get VaultX up and running in 5 minutes!

---

## ⚡ Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and set your SECRET_KEY
# Minimum required: SECRET_KEY
```

### 3. Run the Application
```bash
python app.py
```

### 4. Access VaultX
Open your browser and go to:
```
http://127.0.0.1:8000
```

---

## 🎯 First Steps

### Create an Account
1. Click "Sign Up"
2. Enter username, email, and password
3. Click "Create Account"

### Login
1. Enter your credentials
2. Check your email for OTP (or see terminal if email not configured)
3. Enter OTP to complete login

### Upload a File
1. Drag & drop a file or click to browse
2. Click "Upload & Encrypt"
3. File is automatically encrypted with AES-256

### Explore Features
- **Dashboard** - View your files and recent activity
- **Analytics** - See your usage statistics and charts
- **Search** - Find files and activities quickly
- **Security** - Monitor login attempts and security events
- **Profile** - View your complete activity history
- **Network** - Check system status and network stats

---

## 📧 Enable Email Notifications (Optional)

### Gmail Setup
1. Go to your Google Account: https://myaccount.google.com
2. Enable 2-Factor Authentication
3. Generate App Password:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password

4. Update `.env`:
```env
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-16-char-app-password
```

5. Restart the application

Now you'll receive:
- ✅ Login notifications
- 🚨 Suspicious activity alerts
- 📁 File upload confirmations

---

## 🔐 Security Features

### Automatic Protection
- **AES-256 Encryption** - All files encrypted automatically
- **OTP Authentication** - Two-factor login via email
- **Suspicious Login Detection** - Alerts for unusual activity
- **IP Tracking** - Monitor login locations
- **Failed Attempt Lockout** - Auto-block after 5 failed logins

### Monitor Your Security
1. Go to **Security Dashboard** (`/security`)
2. Review recent security events
3. Check login locations
4. Monitor failed login attempts

---

## 📊 Using Analytics

### View Your Statistics
1. Go to **Analytics Dashboard** (`/analytics`)
2. See your activity over the last 30 days:
   - Total actions
   - Files uploaded/downloaded
   - Login count
   - Activity timeline
   - Hourly patterns

### Generate Reports
- Click on different time periods
- Export data (coming soon)
- Share insights with team

---

## 🔍 Advanced Search

### Search Your Files
1. Go to **Search** (`/search`)
2. Enter search query
3. Select search type:
   - **Files** - Search file names
   - **Activity** - Search all actions
   - **Security** - Search security events

### Use Autocomplete
- Start typing to see suggestions
- Based on your file history
- Click suggestion to search

---

## ⚡ Real-time Updates

### WebSocket Notifications
VaultX automatically shows real-time notifications for:
- 📤 File uploads
- 📥 File downloads
- 🗑️ File deletions
- 🔐 New logins
- ⚠️ Security alerts

No refresh needed - updates appear instantly!

---

## 🗄️ Database Options

### SQLite (Default)
- No setup required
- Works out of the box
- Perfect for development
- Files stored locally

### Supabase (Cloud)
For production or team use:

1. Create Supabase account: https://supabase.com
2. Create new project
3. Get credentials from Settings → API
4. Update `.env`:
```env
DATABASE_TYPE=supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key
```

5. Run database schema:
   - Open Supabase SQL Editor
   - Copy contents of `database/enhanced_schema.sql`
   - Execute

6. Restart application

---

## 🎨 Customization

### Change Upload Limit
Edit `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

### Adjust Rate Limits
Edit `app.py`:
```python
limiter = Limiter(
    app=app,
    default_limits=["500 per day", "100 per hour"]
)
```

### Modify Security Settings
Edit `utils/security.py`:
```python
self.max_failed_attempts = 3  # Stricter
self.lockout_duration = timedelta(minutes=30)  # Longer lockout
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
socketio.run(app, host="127.0.0.1", port=8080, debug=True)
```

### Email Not Sending
- Verify Gmail App Password (not regular password)
- Check spam folder
- Review console for error messages
- Ensure 2FA is enabled on Gmail

### WebSocket Not Connecting
- Check browser console for errors
- Ensure Socket.IO client is loaded
- Try different browser
- Check firewall settings

### Database Errors
- Delete `users.db` and `transfers.db` to reset
- Check file permissions
- Verify disk space

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📱 Browser Support

### Recommended
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+

### Features Requiring Modern Browser
- WebSocket real-time updates
- Drag & drop file upload
- Chart.js visualizations

---

## 🔒 Security Best Practices

### For Users
1. Use strong, unique passwords
2. Don't share your account
3. Review security dashboard regularly
4. Report suspicious activity
5. Keep email account secure

### For Administrators
1. Change default SECRET_KEY
2. Use strong ENCRYPTION_KEY
3. Enable HTTPS in production
4. Regular database backups
5. Monitor security logs
6. Keep dependencies updated
7. Use Supabase for production

---

## 📚 Learn More

### Documentation
- `README.md` - Project overview
- `INTEGRATION_COMPLETE.md` - Feature details
- `ADVANCED_FEATURES_SUMMARY.md` - Feature documentation
- `SUPABASE_SETUP_GUIDE.md` - Supabase setup
- `PROJECT_STRUCTURE.md` - Code organization

### Get Help
- Check documentation files
- Review error messages in console
- Check browser developer tools
- Review security logs

---

## 🎉 You're Ready!

Your VaultX installation is complete. Start uploading files and exploring features!

### Quick Links
- Dashboard: http://127.0.0.1:8000/
- Analytics: http://127.0.0.1:8000/analytics
- Search: http://127.0.0.1:8000/search
- Security: http://127.0.0.1:8000/security

### Next Steps
1. Upload your first file
2. Check analytics dashboard
3. Try the search feature
4. Review security settings
5. Configure email notifications
6. Invite team members (if using Supabase)

---

**Happy Encrypting! 🔐**

*VaultX - Secure File Sharing System*
