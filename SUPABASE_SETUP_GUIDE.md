# VaultX - Supabase Setup Guide

Complete guide to integrate Supabase with VaultX for cloud database and storage.

---

## 📋 Table of Contents

1. [Why Supabase?](#why-supabase)
2. [Prerequisites](#prerequisites)
3. [Step 1: Create Supabase Project](#step-1-create-supabase-project)
4. [Step 2: Get API Keys](#step-2-get-api-keys)
5. [Step 3: Configure Environment](#step-3-configure-environment)
6. [Step 4: Run Database Setup](#step-4-run-database-setup)
7. [Step 5: Update Application](#step-5-update-application)
8. [Step 6: Test Connection](#step-6-test-connection)
9. [Troubleshooting](#troubleshooting)
10. [Migration from SQLite](#migration-from-sqlite)

---

## 🎯 Why Supabase?

**Benefits of using Supabase:**

- ✅ **PostgreSQL Database** - Powerful, scalable relational database
- ✅ **Built-in Authentication** - User management out of the box
- ✅ **File Storage** - Cloud storage for encrypted files
- ✅ **Real-time Subscriptions** - Live data updates
- ✅ **Row Level Security** - Fine-grained access control
- ✅ **Auto-generated APIs** - RESTful and GraphQL APIs
- ✅ **Free Tier** - 500MB database, 1GB storage, 2GB bandwidth
- ✅ **Dashboard** - Easy database management UI

---

## 📦 Prerequisites

- Python 3.8+
- VaultX project installed
- Internet connection
- Email address for Supabase account

---

## Step 1: Create Supabase Project

### 1.1 Sign Up for Supabase

1. Go to [https://supabase.com](https://supabase.com)
2. Click **"Start your project"**
3. Sign up with GitHub, Google, or email
4. Verify your email address

### 1.2 Create New Project

1. Click **"New Project"**
2. Fill in project details:
   - **Name**: `vaultx` (or your preferred name)
   - **Database Password**: Generate a strong password (save it!)
   - **Region**: Choose closest to your users
   - **Pricing Plan**: Free (or Pro if needed)
3. Click **"Create new project"**
4. Wait 2-3 minutes for project setup

---

## Step 2: Get API Keys

### 2.1 Find Your Project Settings

1. In Supabase Dashboard, click **Settings** (gear icon)
2. Navigate to **API** section

### 2.2 Copy Required Keys

You'll need three values:

**1. Project URL**
```
https://xxxxxxxxxxxxx.supabase.co
```

**2. Anon/Public Key** (for client-side)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**3. Service Role Key** (for server-side - keep secret!)
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

⚠️ **Important**: Never commit the Service Role Key to version control!

---

## Step 3: Configure Environment

### 3.1 Update .env File

Open your `.env` file and add:

```bash
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-role-key-here

# Database Type
DATABASE_TYPE=supabase
```

### 3.2 Complete .env Example

```bash
# Flask Application
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=auto-generated-on-first-run

# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-gmail-app-password

# Supabase Configuration
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Database Configuration
DATABASE_TYPE=supabase

# Application Settings
MAX_CONTENT_LENGTH=10485760
FLASK_ENV=development
DEBUG=True
```

---

## Step 4: Run Database Setup

### 4.1 Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `supabase==2.3.4` - Supabase Python client
- `postgrest-py==0.13.2` - PostgreSQL REST client

### 4.2 Run Setup Script

```bash
python supabase_setup.py
```

This will:
- Test your Supabase connection
- Generate `supabase_schema.sql` file
- Display next steps

### 4.3 Execute SQL Schema

1. Open Supabase Dashboard
2. Navigate to **SQL Editor** (left sidebar)
3. Click **"New Query"**
4. Open `supabase_schema.sql` file
5. Copy all contents
6. Paste into SQL Editor
7. Click **"Run"** (or press Ctrl+Enter)

You should see: ✅ `Success. No rows returned`

### 4.4 Verify Tables Created

1. Go to **Table Editor** (left sidebar)
2. You should see three tables:
   - `users`
   - `file_history`
   - `connection_logs`

---

## Step 5: Update Application

### 5.1 Database Adapter (Optional)

The application can use either SQLite or Supabase based on `DATABASE_TYPE` in `.env`.

**For Supabase only**, you can update `app.py` to use `db_supabase.py`:

```python
# At the top of app.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')

if DATABASE_TYPE == 'supabase':
    from db_supabase import (
        create_user as add_user,
        get_user_by_username as get_user,
        log_file_action as log_action,
        get_user_history,
        log_connection as add_connection_log
    )
else:
    # Use existing SQLite functions
    from auth.utils import add_user, get_user
    # ... existing imports
```

### 5.2 File Storage Options

**Option A: Local Storage (Current)**
- Files stored in `server_files/` directory
- Encrypted locally

**Option B: Supabase Storage (Cloud)**
- Files stored in Supabase Storage bucket
- Encrypted before upload
- Use functions from `db_supabase.py`:
  - `upload_encrypted_file()`
  - `download_encrypted_file()`
  - `delete_encrypted_file()`

---

## Step 6: Test Connection

### 6.1 Test Database Connection

```bash
python db_supabase.py
```

Expected output:
```
Testing Supabase connection...
✅ Connection successful!
📊 Stats: {'users': 0, 'file_actions': 0, 'connections': 0}
```

### 6.2 Test Application

```bash
python app.py
```

1. Open http://127.0.0.1:8000
2. Create a new account
3. Login with OTP
4. Upload a file
5. Check Supabase Dashboard > Table Editor > `users` table

You should see your new user!

---

## 🔧 Troubleshooting

### Issue: "Connection test failed"

**Solution:**
1. Verify `SUPABASE_URL` is correct
2. Check `SUPABASE_SERVICE_KEY` is the Service Role key (not Anon key)
3. Ensure project is fully initialized (wait 2-3 minutes after creation)
4. Check internet connection

### Issue: "Table does not exist"

**Solution:**
1. Run the SQL schema in Supabase Dashboard
2. Verify tables exist in Table Editor
3. Check for SQL errors in the query results

### Issue: "Row Level Security policy violation"

**Solution:**
1. Ensure RLS policies are created (in schema SQL)
2. Use Service Role Key for server-side operations
3. Check policy conditions match your use case

### Issue: "Storage bucket not found"

**Solution:**
1. Go to Supabase Dashboard > Storage
2. Create bucket named `encrypted-files`
3. Set to **Private** (not public)
4. Apply storage policies from schema SQL

### Issue: "Import error: No module named 'supabase'"

**Solution:**
```bash
pip install supabase==2.3.4
```

---

## 🔄 Migration from SQLite

### Migrate Existing Users

```python
# migration_script.py
import sqlite3
from db_supabase import create_user

# Connect to SQLite
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Get all users
cursor.execute("SELECT username, email, password FROM users")
users = cursor.fetchall()

# Migrate to Supabase
for username, email, password_hash in users:
    result = create_user(username, email, password_hash)
    if result:
        print(f"✅ Migrated: {username}")
    else:
        print(f"❌ Failed: {username}")

conn.close()
```

Run migration:
```bash
python migration_script.py
```

### Migrate File History

```python
# migration_history.py
import sqlite3
from db_supabase import log_file_action

conn = sqlite3.connect('transfers.db')
cursor = conn.cursor()

cursor.execute("SELECT username, filename, action, ip, timestamp FROM history")
history = cursor.fetchall()

for username, filename, action, ip, timestamp in history:
    log_file_action(username, filename, action, ip)
    print(f"✅ Migrated action: {username} - {action}")

conn.close()
```

---

## 📊 Supabase Dashboard Features

### Table Editor
- View and edit data directly
- Filter and search records
- Export data as CSV

### SQL Editor
- Run custom SQL queries
- Save frequently used queries
- View query history

### Storage
- Browse uploaded files
- Set access policies
- Monitor storage usage

### Database
- View table schemas
- Manage indexes
- Monitor performance

### API Docs
- Auto-generated API documentation
- Test endpoints directly
- View request/response examples

---

## 🚀 Production Deployment

### Environment Variables

Set these in your production environment:

```bash
DATABASE_TYPE=supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key
SECRET_KEY=strong-random-key
ENCRYPTION_KEY=your-encryption-key
FLASK_ENV=production
DEBUG=False
```

### Security Checklist

- [ ] Use Service Role Key (not Anon key) for server operations
- [ ] Enable Row Level Security on all tables
- [ ] Set up proper RLS policies
- [ ] Use HTTPS for all connections
- [ ] Rotate keys regularly
- [ ] Monitor API usage in Supabase Dashboard
- [ ] Set up database backups
- [ ] Configure rate limiting

### Performance Optimization

1. **Indexes**: Already created in schema
2. **Connection Pooling**: Supabase handles this
3. **Caching**: Consider Redis for frequently accessed data
4. **CDN**: Use Supabase CDN for storage files

---

## 📈 Monitoring

### Supabase Dashboard Metrics

- **Database**: Query performance, connections
- **Storage**: Usage, bandwidth
- **Auth**: User signups, logins
- **API**: Request count, response times

### Application Logs

Monitor in your Flask app:
- Database query times
- API response codes
- Error rates
- User activity

---

## 💰 Pricing

### Free Tier Limits
- 500 MB database space
- 1 GB file storage
- 2 GB bandwidth
- 50,000 monthly active users
- Unlimited API requests

### When to Upgrade
- Database > 500 MB
- Storage > 1 GB
- Need daily backups
- Require custom domains
- Need priority support

---

## 🔗 Useful Links

- **Supabase Docs**: https://supabase.com/docs
- **Python Client**: https://github.com/supabase-community/supabase-py
- **Dashboard**: https://app.supabase.com
- **Status Page**: https://status.supabase.com
- **Community**: https://github.com/supabase/supabase/discussions

---

## ✅ Setup Checklist

- [ ] Created Supabase account
- [ ] Created new project
- [ ] Copied API keys
- [ ] Updated .env file
- [ ] Installed dependencies (`pip install -r requirements.txt`)
- [ ] Ran `python supabase_setup.py`
- [ ] Executed SQL schema in Supabase Dashboard
- [ ] Verified tables created
- [ ] Tested connection (`python db_supabase.py`)
- [ ] Updated `DATABASE_TYPE=supabase` in .env
- [ ] Tested application
- [ ] Created test user
- [ ] Uploaded test file
- [ ] Verified data in Supabase Dashboard

---

## 🎉 Success!

Your VaultX application is now connected to Supabase!

**Benefits you now have:**
- ✅ Cloud PostgreSQL database
- ✅ Scalable file storage
- ✅ Real-time capabilities
- ✅ Built-in authentication
- ✅ Automatic backups (Pro plan)
- ✅ Global CDN
- ✅ Easy database management

**Next Steps:**
1. Migrate existing data (if any)
2. Test all features thoroughly
3. Set up monitoring
4. Configure production environment
5. Deploy your application

---

**Need Help?**
- Check [Troubleshooting](#troubleshooting) section
- Review Supabase documentation
- Check application logs
- Test connection with `python db_supabase.py`

---

*Last Updated: May 5, 2026*  
*VaultX Version: 2.0*
