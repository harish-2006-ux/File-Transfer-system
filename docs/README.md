# VaultX Documentation

Complete documentation for the VaultX Secure File Sharing System.

## Quick Links

- **[Quick Start](./QUICKSTART.md)** - Get started in 5 minutes
- **[Setup Guide](./SETUP.md)** - Detailed setup instructions
- **[API Reference](./API.md)** - API endpoints documentation
- **[Architecture](./ARCHITECTURE.md)** - System architecture overview
- **[Deployment](./DEPLOYMENT.md)** - Production deployment guide

## Documentation Files

### Getting Started
- `QUICKSTART.md` - 5-minute quick start guide
- `SETUP.md` - Detailed setup and configuration
- `INSTALLATION.md` - Installation instructions

### Development
- `ARCHITECTURE.md` - System architecture
- `API.md` - API endpoints reference
- `DATABASE.md` - Database schema and operations
- `SECURITY.md` - Security features and best practices

### Operations
- `DEPLOYMENT.md` - Production deployment
- `TROUBLESHOOTING.md` - Common issues and solutions
- `MAINTENANCE.md` - Maintenance and monitoring

### Supabase
- `SUPABASE.md` - Supabase integration guide
- `SUPABASE_QUICKSTART.md` - 5-minute Supabase setup

## Project Structure

```
vaultx/
├── app.py                 # Main Flask application
├── config/                # Configuration module
├── database/              # Database layer
├── utils/                 # Utility functions
├── auth/                  # Authentication (legacy)
├── services/              # Services (legacy)
├── templates/             # HTML templates
├── static/                # Static assets
├── storage/               # File storage
├── frontend/              # React frontend
└── docs/                  # Documentation
```

## Key Features

- 🔐 AES-256 file encryption
- 🔑 Two-factor authentication (Email OTP)
- 📊 Activity tracking and audit logs
- 📈 Real-time system monitoring
- ☁️ Cloud database support (Supabase)
- 🎨 Modern glassmorphism UI

## Technology Stack

**Backend:**
- Flask 3.0.3
- Supabase (PostgreSQL)
- Bcrypt + OTP
- AES-256 Fernet

**Frontend:**
- React 18.3.1
- Vite 5.4.1
- Tailwind CSS
- Framer Motion

## Getting Help

1. Check the relevant documentation file
2. Review troubleshooting guide
3. Check application logs
4. Test with minimal setup

## Contributing

When adding new features:
1. Update relevant documentation
2. Add code comments
3. Update API reference if needed
4. Test thoroughly

---

**Version:** 2.0  
**Last Updated:** May 5, 2026
