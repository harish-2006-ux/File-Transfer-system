# VaultX Project Structure

Perfect folder organization for the VaultX Secure File Sharing System.

---

## 📁 Complete Directory Structure

```
vaultx/
│
├── 📄 Core Application Files
│   ├── app.py                      # Main Flask application
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # Environment variables (local)
│   ├── .env.example                # Environment template
│   └── .gitignore                  # Git ignore rules
│
├── 📁 config/                      # Configuration Module
│   ├── __init__.py                 # Package init
│   └── settings.py                 # Configuration settings
│
├── 📁 database/                    # Database Layer
│   ├── __init__.py                 # Package init
│   ├── supabase_client.py          # Supabase client interface
│   ├── setup.py                    # Database setup script
│   └── schema.sql                  # Database schema (auto-generated)
│
├── 📁 utils/                       # Utility Functions
│   ├── __init__.py                 # Package init
│   ├── encryption.py               # File encryption/decryption
│   └── auth.py                     # Authentication utilities
│
├── 📁 auth/                        # Authentication (Legacy)
│   ├── __init__.py                 # Package init
│   └── utils.py                    # Auth utilities (deprecated)
│
├── 📁 services/                    # Services (Legacy)
│   ├── __init__.py                 # Package init
│   └── encryption.py               # Encryption service (deprecated)
│
├── 📁 templates/                   # HTML Templates
│   ├── login.html                  # Login page
│   ├── signup.html                 # Registration page
│   ├── otp_verify.html             # OTP verification
│   ├── home.html                   # Dashboard
│   ├── profile.html                # User profile
│   └── network.html                # Network monitoring
│
├── 📁 static/                      # Static Assets
│   └── style.css                   # Glassmorphism styling
│
├── 📁 storage/                     # File Storage
│   └── encrypted_files/            # Encrypted files directory
│
├── 📁 frontend/                    # React Frontend (Optional)
│   ├── src/
│   │   ├── App.jsx                 # Main React component
│   │   ├── main.jsx                # Entry point
│   │   ├── index.css               # Global styles
│   │   └── NetworkDashboard.jsx    # Dashboard component
│   ├── public/                     # Public assets
│   ├── package.json                # Frontend dependencies
│   ├── vite.config.js              # Vite configuration
│   ├── tailwind.config.js          # Tailwind configuration
│   └── postcss.config.js           # PostCSS configuration
│
├── 📁 docs/                        # Documentation
│   ├── README.md                   # Documentation index
│   ├── QUICKSTART.md               # Quick start guide
│   ├── SETUP.md                    # Setup instructions
│   ├── API.md                      # API reference
│   ├── ARCHITECTURE.md             # Architecture overview
│   ├── DATABASE.md                 # Database documentation
│   ├── SECURITY.md                 # Security guide
│   ├── DEPLOYMENT.md               # Deployment guide
│   ├── TROUBLESHOOTING.md          # Troubleshooting
│   └── SUPABASE.md                 # Supabase guide
│
├── 📄 Root Documentation
│   ├── README.md                   # Project overview
│   ├── PROJECT_STRUCTURE.md        # This file
│   ├── PROJECT_REPORT.md           # Comprehensive report
│   ├── STATUS.md                   # Current status
│   ├── OPTIMIZATION_SUMMARY.md     # Performance improvements
│   ├── TODO.md                     # Development checklist
│   └── TODO_optimize.md            # Optimization checklist
│
├── 📁 .git/                        # Git repository
├── 📁 .vscode/                     # VS Code settings
├── 📁 __pycache__/                 # Python cache (ignored)
└── 📁 node_modules/                # Node dependencies (ignored)
```

---

## 📋 File Organization Guide

### Core Application (`/`)
- **app.py** - Main Flask application with all routes
- **requirements.txt** - Python package dependencies
- **.env** - Local environment variables (not in git)
- **.env.example** - Template for environment variables

### Configuration (`/config`)
- **settings.py** - Centralized configuration for all environments
- Supports: Development, Production, Testing

### Database (`/database`)
- **supabase_client.py** - Supabase database interface
- **setup.py** - Database initialization script
- **schema.sql** - Database schema (auto-generated)

### Utilities (`/utils`)
- **encryption.py** - AES-256 file encryption/decryption
- **auth.py** - Password hashing, OTP, user management

### Templates (`/templates`)
- Jinja2 HTML templates for all pages
- Responsive design with glassmorphism

### Static Assets (`/static`)
- **style.css** - Custom CSS styling
- Glassmorphism design system

### File Storage (`/storage`)
- **encrypted_files/** - Directory for encrypted files
- User-specific subdirectories

### Frontend (`/frontend`)
- React application with Vite
- Optional - can run separately
- Tailwind CSS for styling

### Documentation (`/docs`)
- Comprehensive guides and references
- API documentation
- Setup and deployment guides

---

## 🔄 Module Dependencies

```
app.py
├── config/settings.py
├── database/supabase_client.py
├── utils/encryption.py
├── utils/auth.py
├── templates/*.html
└── static/style.css

database/supabase_client.py
└── (Supabase SDK)

utils/encryption.py
└── (cryptography library)

utils/auth.py
├── database/supabase_client.py
├── (bcrypt library)
└── (smtplib - standard library)

frontend/
├── React
├── Vite
├── Tailwind CSS
└── Framer Motion
```

---

## 📦 What Each Folder Contains

### `/config`
Configuration management for different environments.
- Development: Debug mode, insecure cookies
- Production: Secure settings, Redis rate limiting
- Testing: Test database, test mode

### `/database`
All database-related code.
- Client initialization
- CRUD operations
- Schema management
- Connection pooling

### `/utils`
Reusable utility functions.
- Encryption/decryption
- Password hashing
- OTP generation
- Email sending

### `/templates`
HTML templates rendered by Flask.
- Login/signup forms
- Dashboard
- File management
- User profile
- Network monitoring

### `/static`
Static files served directly.
- CSS stylesheets
- Client-side JavaScript
- Images and fonts

### `/storage`
File storage directory.
- Encrypted files
- User-specific subdirectories
- Temporary files during processing

### `/frontend`
Optional React frontend.
- Can run independently
- Communicates with Flask API
- Real-time dashboard

### `/docs`
Complete documentation.
- Setup guides
- API reference
- Architecture overview
- Troubleshooting

---

## 🚀 How to Use This Structure

### Adding a New Feature

1. **Backend Logic** → `/utils` or `/database`
2. **Configuration** → `/config/settings.py`
3. **Template** → `/templates/new_page.html`
4. **Styling** → `/static/style.css`
5. **Route** → `app.py`
6. **Documentation** → `/docs/`

### Adding a New Utility

1. Create file in `/utils/`
2. Add to `/utils/__init__.py`
3. Import in `app.py` or other modules
4. Document in `/docs/`

### Adding Database Operations

1. Add function to `/database/supabase_client.py`
2. Export from `/database/__init__.py`
3. Use in `app.py` or other modules
4. Document in `/docs/DATABASE.md`

---

## 🔐 Security Considerations

### Sensitive Files (Not in Git)
- `.env` - Environment variables
- `storage/encrypted_files/` - Encrypted user files
- `__pycache__/` - Python cache
- `node_modules/` - Node dependencies

### Protected Directories
- `/database` - Database credentials
- `/config` - Sensitive settings
- `/utils/auth.py` - Password handling

### Public Directories
- `/templates` - HTML templates
- `/static` - CSS and client-side assets
- `/docs` - Documentation
- `/frontend` - React frontend

---

## 📊 File Statistics

| Directory | Purpose | Files |
|-----------|---------|-------|
| `/config` | Configuration | 2 |
| `/database` | Database layer | 3 |
| `/utils` | Utilities | 2 |
| `/templates` | HTML templates | 6 |
| `/static` | CSS/JS | 1 |
| `/storage` | File storage | 1 |
| `/frontend` | React app | 6+ |
| `/docs` | Documentation | 10+ |
| Root | Core files | 5 |

---

## 🔄 Migration from Old Structure

### Old → New Mapping

| Old Location | New Location | Status |
|-------------|-------------|--------|
| `db_init.py` | `database/setup.py` | ✅ Moved |
| `db.py` | Removed | ✅ Deleted |
| `db_supabase.py` | `database/supabase_client.py` | ✅ Moved |
| `supabase_setup.py` | `database/setup.py` | ✅ Moved |
| `models.py` | Removed | ✅ Deleted |
| `auth/utils.py` | `utils/auth.py` | ✅ Moved |
| `services/encryption.py` | `utils/encryption.py` | ✅ Moved |
| `*.db` files | Removed | ✅ Deleted |

---

## 🎯 Best Practices

### Imports
```python
# Good
from config.settings import Config
from database import get_supabase
from utils.encryption import encrypt_file

# Avoid
from database.supabase_client import get_supabase
```

### File Organization
- Keep related code together
- Use `__init__.py` for package exports
- One responsibility per module

### Documentation
- Document new modules in `/docs/`
- Update `PROJECT_STRUCTURE.md` when adding folders
- Keep README files in each major folder

### Configuration
- Use `/config/settings.py` for all settings
- Never hardcode credentials
- Use environment variables

---

## 📝 Adding New Folders

When adding a new folder:

1. Create folder with `__init__.py`
2. Add to this document
3. Update `/docs/README.md`
4. Document purpose and contents
5. Add to `.gitignore` if needed

---

## ✅ Verification Checklist

- [x] All old files removed
- [x] New structure created
- [x] Imports updated
- [x] Configuration centralized
- [x] Database layer organized
- [x] Utilities separated
- [x] Documentation organized
- [x] No duplicate files
- [x] Clean and logical structure

---

**Status**: ✅ Complete  
**Version**: 2.0  
**Last Updated**: May 5, 2026

*VaultX - Clean, Organized, Production-Ready* 🚀
