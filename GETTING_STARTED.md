# VaultX - Getting Started Guide

Quick reference for getting started with VaultX.

---

## ⚡ 5-Minute Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run Application
```bash
python app.py
```

### 4. Access Application
- **Backend**: http://127.0.0.1:8000
- **Frontend**: http://localhost:3000 (optional)

---

## 📋 First Time Setup Checklist

### Prerequisites
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed (optional)
- [ ] Git installed
- [ ] Text editor ready

### Installation
- [ ] Clone/download project
- [ ] Navigate to project directory
- [ ] Run `pip install -r requirements.txt`
- [ ] Copy `.env.example` to `.env`

### Configuration
- [ ] Edit `.env` file
- [ ] Set `SECRET_KEY` (generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- [ ] Set `SENDER_EMAIL` and `SENDER_PASSWORD` (for OTP)
- [ ] Set `SUPABASE_URL` and `SUPABASE_KEY` (optional, for cloud)

### Running
- [ ] Start backend: `python app.py`
- [ ] Start frontend: `cd frontend && npm install && npm run dev` (optional)
- [ ] Open http://127.0.0.1:8000 in browser
- [ ] Test login/signup

### Verification
- [ ] Can access login page
- [ ] Can create account
- [ ] Can receive OTP (check terminal or email)
- [ ] Can login successfully
- [ ] Can upload file
- [ ] Can download file
- [ ] Can view dashboard

---

## 🔧 Configuration Guide

### Essential Settings (.env)

```bash
# Flask Application
SECRET_KEY=your-secret-key-here

# Encryption
ENCRYPTION_KEY=auto-generated-on-first-run

# Email (for OTP)
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-gmail-app-password

# Database (optional - Supabase)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
```

### Generate Secret Key
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Gmail App Password
1. Enable 2FA on Gmail
2. Go to Google Account > Security > App Passwords
3. Generate new app password
4. Use in `SENDER_PASSWORD`

---

## 📚 Documentation Quick Links

### Getting Started
- **[README.md](README.md)** - Main overview
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - This file
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - 5-minute setup

### Setup & Configuration
- **[docs/SETUP.md](docs/SETUP.md)** - Detailed setup
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Folder organization
- **[config/settings.py](config/settings.py)** - Configuration file

### Features & Usage
- **[docs/API.md](docs/API.md)** - API endpoints
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design
- **[docs/DATABASE.md](docs/DATABASE.md)** - Database info

### Deployment & Operations
- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Production setup
- **[docs/SECURITY.md](docs/SECURITY.md)** - Security features
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues

### Supabase Integration
- **[docs/SUPABASE.md](docs/SUPABASE.md)** - Cloud database setup
- **[SUPABASE_QUICKSTART.md](SUPABASE_QUICKSTART.md)** - 5-min Supabase setup

---

## 🚀 Common Tasks

### Start Backend
```bash
python app.py
```

### Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### Setup Supabase Database
```bash
python database/setup.py
# Then execute SQL in Supabase Dashboard
```

### Test Connection
```bash
python database/setup.py
```

### Generate Encryption Key
```bash
python -c "from utils.encryption import get_key; print(get_key().decode())"
```

---

## 🔐 Security Reminders

- ✅ Never commit `.env` file
- ✅ Use strong `SECRET_KEY`
- ✅ Keep `SUPABASE_SERVICE_KEY` secret
- ✅ Use Gmail app password (not main password)
- ✅ Enable 2FA on Gmail
- ✅ Rotate keys regularly
- ✅ Use HTTPS in production
- ✅ Keep dependencies updated

---

## 🧪 Testing

### Test User Registration
1. Go to http://127.0.0.1:8000/signup
2. Enter username, email, password
3. Click "Sign Up"
4. Should redirect to login

### Test Login
1. Go to http://127.0.0.1:8000/login
2. Enter credentials
3. Check terminal for OTP (or email)
4. Enter OTP
5. Should access dashboard

### Test File Upload
1. On dashboard, click "Choose File"
2. Select a file
3. Click "Upload"
4. File should appear in list

### Test File Download
1. Click filename in list
2. File should download
3. Check it's decrypted correctly

### Test File Delete
1. Click "Delete" next to filename
2. File should be removed from list

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(port=8001)
```

### Email OTP Not Sending
- Check SENDER_EMAIL and SENDER_PASSWORD
- Verify Gmail app password
- Check spam folder
- Use terminal OTP for testing

### Database Connection Error
- Verify Supabase credentials
- Check internet connection
- Test with: `python database/setup.py`

### File Upload Fails
- Check file size (<10MB)
- Verify storage/encrypted_files/ exists
- Check disk space

### Import Errors
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version (3.8+)
- Verify virtual environment

---

## 📞 Getting Help

### Check Documentation
1. Read relevant guide in `/docs/`
2. Check [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
3. Review [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

### Check Logs
1. Look at terminal output
2. Check application logs
3. Review error messages

### Test Manually
1. Test with minimal setup
2. Test each feature separately
3. Check configuration

---

## 🎯 Next Steps

### After Setup
1. ✅ Review [README.md](README.md)
2. ✅ Explore [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
3. ✅ Test all features
4. ✅ Read [docs/SECURITY.md](docs/SECURITY.md)

### For Development
1. ✅ Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
2. ✅ Review [docs/API.md](docs/API.md)
3. ✅ Check [docs/DATABASE.md](docs/DATABASE.md)
4. ✅ Start coding!

### For Production
1. ✅ Read [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
2. ✅ Setup Supabase: [docs/SUPABASE.md](docs/SUPABASE.md)
3. ✅ Configure security
4. ✅ Deploy!

---

## 📊 Project Structure Overview

```
vaultx/
├── app.py                 # Main application
├── config/                # Configuration
├── database/              # Database layer
├── utils/                 # Utilities
├── templates/             # HTML templates
├── static/                # CSS/assets
├── storage/               # File storage
├── frontend/              # React frontend
├── docs/                  # Documentation
└── README.md              # Main guide
```

See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) for details.

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] Backend running
- [ ] Can access login page
- [ ] Can create account
- [ ] Can login with OTP
- [ ] Can upload file
- [ ] Can download file
- [ ] Can delete file
- [ ] Dashboard working
- [ ] All features tested

---

## 🎉 You're Ready!

VaultX is now set up and ready to use!

**Next**: Read [README.md](README.md) for complete overview.

---

**Version**: 2.0  
**Status**: ✅ Ready to Use  
**Date**: May 5, 2026

*VaultX - Secure, Fast, Cloud-Ready* 🚀
