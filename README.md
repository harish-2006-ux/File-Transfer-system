# 🔐 VaultX - Secure File Transfer System

[![Live Demo](https://img.shields.io/badge/Live%20Demo-VaultX-00c8ff?style=for-the-badge&logo=render)](https://vaultx-fgjr.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> **Secure, encrypted file transfer system with AES-256 encryption, two-factor authentication, and beautiful cyberpunk UI**

## 🌐 Live Demo

**🚀 [Try VaultX Now](https://vaultx-fgjr.onrender.com)**

### Test Credentials:
- **Username:** `testuser` | **Password:** `Test123!`
- **Username:** `harishvm123` | **Password:** `Test123!`

---

## ✨ Features

### 🔒 Security
- **AES-256 Encryption** - Military-grade file encryption
- **Two-Factor Authentication** - OTP verification via email
- **Secure Password Hashing** - bcrypt with salt
- **Session Management** - Secure user sessions
- **Activity Logging** - Track all file operations

### 📁 File Management
- **Drag & Drop Upload** - Intuitive file upload interface
- **Encrypted Storage** - All files encrypted at rest
- **Secure Download** - Decrypt files on-the-fly
- **File Sharing** - Share files via email with HTML templates
- **File Search** - Quick search through your files

### 🎨 User Interface
- **Cyberpunk Design** - Beautiful glassmorphism effects
- **Animated Starfield** - Dynamic background animations
- **Responsive Layout** - Works on all devices
- **Real-time Updates** - Live statistics and notifications
- **Professional Typography** - Outfit + JetBrains Mono fonts

### 📊 Dashboard Features
- **File Statistics** - Track encrypted files and transfers
- **Activity Feed** - Recent file operations
- **Live Clock** - Real-time system clock
- **Server Status** - Live server monitoring
- **Upload Progress** - Visual upload feedback

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Gmail account (for OTP emails)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/harish-2006-ux/File-Transfer-system.git
cd File-Transfer-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the application**
```bash
python app.py
```

5. **Access VaultX**
```
http://localhost:8000
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=False

# Email Configuration (Gmail)
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-gmail-app-password

# Encryption
ENCRYPTION_KEY=your-encryption-key-here

# Database (Optional)
DATABASE_TYPE=sqlite
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

### Gmail App Password Setup

1. Enable 2-Factor Authentication on your Gmail account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate a new app password for "Mail"
4. Use the 16-character password in your `.env` file

---

## 🏗️ Tech Stack

### Backend
- **Flask 3.0** - Python web framework
- **SQLite** - Local database
- **Supabase** - Optional cloud database
- **bcrypt** - Password hashing
- **cryptography** - AES-256 encryption
- **Gunicorn** - Production WSGI server

### Frontend
- **HTML5/CSS3** - Modern web standards
- **Vanilla JavaScript** - No framework dependencies
- **Google Fonts** - Outfit & JetBrains Mono
- **CSS Animations** - Smooth transitions and effects

### Deployment
- **Render** - Backend hosting
- **Vercel** - Frontend hosting (optional)
- **GitHub Actions** - CI/CD (optional)

---

## 📂 Project Structure

```
VaultX/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment config
├── runtime.txt           # Python version
├── .env                  # Environment variables (not in git)
├── .env.example          # Environment template
│
├── templates/            # HTML templates
│   ├── login.html       # Login page
│   ├── signup.html      # Registration page
│   ├── otp_verify.html  # OTP verification
│   ├── home.html        # Main dashboard
│   └── error.html       # Error pages
│
├── static/              # Static assets
│   └── style.css        # Cyberpunk styling
│
├── server_files/        # Encrypted file storage
│
└── README.md           # This file
```

---

## 🔐 Security Features

### Encryption
- **Algorithm:** AES-256 (Fernet)
- **Key Management:** Environment-based keys
- **File Storage:** All files encrypted at rest
- **Secure Transmission:** HTTPS in production

### Authentication
- **Password Hashing:** bcrypt with automatic salt
- **Two-Factor Auth:** Email-based OTP verification
- **Session Security:** Secure session cookies
- **Rate Limiting:** Protection against brute force

### Best Practices
- ✅ No passwords stored in plain text
- ✅ Environment variables for secrets
- ✅ HTTPS enforced in production
- ✅ Input validation and sanitization
- ✅ SQL injection prevention
- ✅ XSS protection

---

## 🎨 Screenshots

### Login Page
Beautiful cyberpunk-themed login with glassmorphism effects and animated starfield background.

### Dashboard
Professional file management interface with drag & drop upload, real-time statistics, and activity feed.

### File Sharing
Share encrypted files via email with professional HTML templates.

---

## 🚀 Deployment

### Deploy to Render

1. **Fork this repository**
2. **Create a new Web Service** on [Render](https://render.com)
3. **Connect your GitHub repository**
4. **Add environment variables** in Render dashboard
5. **Deploy!**

Render will automatically:
- Install dependencies from `requirements.txt`
- Use Python version from `runtime.txt`
- Start the app using `Procfile`

### Deploy to Vercel (Frontend)

```bash
cd frontend
vercel deploy
```

---

## 📝 API Endpoints

### Authentication
- `GET /` - Home page (redirects to dashboard if logged in)
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /signup` - Registration page
- `POST /signup` - Create account
- `GET /verify-otp` - OTP verification page
- `POST /verify-otp` - Verify OTP
- `GET /logout` - Logout user

### File Operations
- `GET /dashboard` - Main dashboard
- `POST /upload` - Upload and encrypt file
- `GET /download/<filename>` - Download and decrypt file
- `POST /share/<filename>` - Share file via email
- `GET /delete/<filename>` - Delete file

### Additional Pages
- `GET /network` - Network monitoring (coming soon)
- `GET /profile` - User profile (coming soon)
- `GET /analytics` - Analytics dashboard (coming soon)
- `GET /search` - File search (coming soon)
- `GET /security` - Security settings (coming soon)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Harish VM**
- GitHub: [@harish-2006-ux](https://github.com/harish-2006-ux)
- Email: hhareeshvm@gmail.com

---

## 🙏 Acknowledgments

- Flask framework and community
- Render for hosting
- Google Fonts for typography
- Cryptography library for encryption
- All contributors and testers

---

## 📊 Project Status

- ✅ **Core Features:** Complete
- ✅ **Security:** AES-256 + 2FA
- ✅ **UI/UX:** Cyberpunk design
- ✅ **Deployment:** Live on Render
- 🚧 **Advanced Features:** In development
- 🚧 **Mobile App:** Planned

---

## 🔗 Links

- **Live Demo:** https://vaultx-fgjr.onrender.com
- **Repository:** https://github.com/harish-2006-ux/File-Transfer-system
- **Issues:** https://github.com/harish-2006-ux/File-Transfer-system/issues
- **Documentation:** Coming soon

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Made with ❤️ by Harish VM**

</div>