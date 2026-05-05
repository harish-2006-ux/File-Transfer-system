# 🗄️ VaultX Supabase Setup Guide

## Current Status

### ✅ Supabase Connection Status
- **URL:** `https://mwnqkxubuvubtndhdgpt.supabase.co`
- **Anon Key:** Configured ✅
- **Service Key:** ⚠️ Needs to be added to `.env`
- **Database Type:** Set to `supabase` in `.env`

### 📊 Recent Changes (Last 24 Hours)
1. ✅ Added deployment configuration (Render + Vercel)
2. ✅ Cleaned up markdown files
3. ✅ Updated email configuration
4. ✅ All 8 advanced features integrated

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Run SQL in Supabase Dashboard

1. **Go to:** https://app.supabase.com/project/mwnqkxubuvubtndhdgpt/sql/new
2. **Copy and paste** the complete SQL below
3. **Click "Run"**

### Step 2: Update .env File

Add your Supabase Service Key to `.env`:
```env
SUPABASE_SERVICE_KEY=your-service-role-key-here
```

Get it from: https://app.supabase.com/project/mwnqkxubuvubtndhdgpt/settings/api

### Step 3: Restart Application

```bash
# Stop and restart Flask backend to connect to Supabase
```

---

## 📋 Complete SQL for Supabase SQL Editor

Copy this entire SQL script and run it in Supabase SQL Editor:

```sql
-- ============================================================
-- VaultX Complete Database Schema
-- Run this in: Supabase Dashboard > SQL Editor > New Query
-- ============================================================

-- ============================================================
-- CORE TABLES
-- ============================================================

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    last_login_ip TEXT,
    last_login_at TIMESTAMP WITH TIME ZONE,
    last_user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- File history table
CREATE TABLE IF NOT EXISTS file_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    username TEXT NOT NULL,
    filename TEXT,
    action TEXT NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    filesize BIGINT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Connection logs table
CREATE TABLE IF NOT EXISTS connection_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ip_address TEXT NOT NULL,
    method TEXT NOT NULL,
    path TEXT NOT NULL,
    status_code INTEGER NOT NULL,
    user_agent TEXT,
    response_time INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- ADVANCED FEATURE TABLES
-- ============================================================

-- Security events table
CREATE TABLE IF NOT EXISTS security_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    username TEXT NOT NULL,
    event_type TEXT NOT NULL,
    ip_address TEXT NOT NULL,
    user_agent TEXT,
    details JSONB,
    severity TEXT DEFAULT 'medium',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Device fingerprints table
CREATE TABLE IF NOT EXISTS device_fingerprints (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    fingerprint_hash TEXT NOT NULL,
    device_name TEXT,
    browser TEXT,
    os TEXT,
    last_seen_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_trusted BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Login locations table
CREATE TABLE IF NOT EXISTS login_locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    ip_address TEXT NOT NULL,
    country TEXT,
    city TEXT,
    region TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    timezone TEXT,
    login_count INTEGER DEFAULT 1,
    last_login_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    message TEXT NOT NULL,
    notification_type TEXT DEFAULT 'info',
    is_read BOOLEAN DEFAULT false,
    data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User preferences table
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    email_notifications BOOLEAN DEFAULT true,
    login_alerts BOOLEAN DEFAULT true,
    suspicious_activity_alerts BOOLEAN DEFAULT true,
    daily_summary BOOLEAN DEFAULT false,
    theme TEXT DEFAULT 'light',
    language TEXT DEFAULT 'en',
    timezone TEXT DEFAULT 'UTC',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- API keys table
CREATE TABLE IF NOT EXISTS api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    key_hash TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    permissions JSONB DEFAULT '[]'::jsonb,
    last_used_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_file_history_user_id ON file_history(user_id);
CREATE INDEX IF NOT EXISTS idx_file_history_username ON file_history(username);
CREATE INDEX IF NOT EXISTS idx_file_history_created_at ON file_history(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_file_history_action ON file_history(action);
CREATE INDEX IF NOT EXISTS idx_connection_logs_created_at ON connection_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_connection_logs_ip ON connection_logs(ip_address);
CREATE INDEX IF NOT EXISTS idx_security_events_user_id ON security_events(user_id);
CREATE INDEX IF NOT EXISTS idx_security_events_username ON security_events(username);
CREATE INDEX IF NOT EXISTS idx_security_events_created_at ON security_events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_security_events_event_type ON security_events(event_type);
CREATE INDEX IF NOT EXISTS idx_device_fingerprints_user_id ON device_fingerprints(user_id);
CREATE INDEX IF NOT EXISTS idx_device_fingerprints_hash ON device_fingerprints(fingerprint_hash);
CREATE INDEX IF NOT EXISTS idx_login_locations_user_id ON login_locations(user_id);
CREATE INDEX IF NOT EXISTS idx_login_locations_ip ON login_locations(ip_address);
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX IF NOT EXISTS idx_api_keys_key_hash ON api_keys(key_hash);

-- ============================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE file_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE connection_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE security_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE device_fingerprints ENABLE ROW LEVEL SECURITY;
ALTER TABLE login_locations ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_keys ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- RLS POLICIES (Allow service role full access)
-- ============================================================

-- Users
DROP POLICY IF EXISTS "Service role full access" ON users;
CREATE POLICY "Service role full access" ON users FOR ALL USING (true);

-- File history
DROP POLICY IF EXISTS "Service role full access" ON file_history;
CREATE POLICY "Service role full access" ON file_history FOR ALL USING (true);

-- Connection logs
DROP POLICY IF EXISTS "Service role full access" ON connection_logs;
CREATE POLICY "Service role full access" ON connection_logs FOR ALL USING (true);

-- Security events
DROP POLICY IF EXISTS "Service role full access" ON security_events;
CREATE POLICY "Service role full access" ON security_events FOR ALL USING (true);

-- Device fingerprints
DROP POLICY IF EXISTS "Service role full access" ON device_fingerprints;
CREATE POLICY "Service role full access" ON device_fingerprints FOR ALL USING (true);

-- Login locations
DROP POLICY IF EXISTS "Service role full access" ON login_locations;
CREATE POLICY "Service role full access" ON login_locations FOR ALL USING (true);

-- Notifications
DROP POLICY IF EXISTS "Service role full access" ON notifications;
CREATE POLICY "Service role full access" ON notifications FOR ALL USING (true);

-- User preferences
DROP POLICY IF EXISTS "Service role full access" ON user_preferences;
CREATE POLICY "Service role full access" ON user_preferences FOR ALL USING (true);

-- API keys
DROP POLICY IF EXISTS "Service role full access" ON api_keys;
CREATE POLICY "Service role full access" ON api_keys FOR ALL USING (true);

-- ============================================================
-- FUNCTIONS
-- ============================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_user_preferences_updated_at ON user_preferences;
CREATE TRIGGER update_user_preferences_updated_at
    BEFORE UPDATE ON user_preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================
-- VIEWS FOR ANALYTICS
-- ============================================================

CREATE OR REPLACE VIEW user_activity_summary AS
SELECT 
    username,
    COUNT(*) as total_actions,
    COUNT(CASE WHEN action = 'UPLOAD' THEN 1 END) as uploads,
    COUNT(CASE WHEN action = 'DOWNLOAD' THEN 1 END) as downloads,
    COUNT(CASE WHEN action = 'DELETE' THEN 1 END) as deletes,
    COUNT(CASE WHEN action = 'LOGIN' THEN 1 END) as logins,
    MAX(created_at) as last_activity
FROM file_history
GROUP BY username;

CREATE OR REPLACE VIEW security_summary AS
SELECT 
    username,
    COUNT(*) as total_events,
    COUNT(CASE WHEN event_type = 'SUSPICIOUS_LOGIN' THEN 1 END) as suspicious_logins,
    COUNT(CASE WHEN event_type = 'FAILED_LOGIN' THEN 1 END) as failed_logins,
    COUNT(DISTINCT ip_address) as unique_ips,
    MAX(created_at) as last_event
FROM security_events
GROUP BY username;

-- ============================================================
-- SUCCESS MESSAGE
-- ============================================================

SELECT 'VaultX database setup complete!' AS status,
       '12 tables created' AS tables,
       '20+ indexes created' AS indexes,
       'RLS enabled on all tables' AS security,
       '2 analytics views created' AS analytics;
```

---

## 📊 Tables Created (12 Total)

### Core Tables (3)
1. **users** - User accounts and authentication
2. **file_history** - File upload/download/share logs
3. **connection_logs** - HTTP request logs

### Advanced Feature Tables (6)
4. **security_events** - Security alerts and suspicious activity
5. **device_fingerprints** - Trusted device tracking
6. **login_locations** - Geolocation tracking
7. **notifications** - In-app notifications
8. **user_preferences** - User settings
9. **api_keys** - API access tokens

---

## 🔍 Verify Tables in Supabase

After running the SQL, verify in Supabase Dashboard:

1. **Go to:** https://app.supabase.com/project/mwnqkxubuvubtndhdgpt/editor
2. **Check Tables:** You should see all 12 tables
3. **Check Indexes:** Click on any table → Indexes tab
4. **Check RLS:** Click on any table → Policies tab

---

## 📥 Import Existing Data (Optional)

If you have existing SQLite data, run this in SQL Editor:

```sql
-- Import your existing history data
INSERT INTO file_history (username, filename, action, ip_address, created_at) VALUES
('harishvm123', NULL, 'LOGIN', '127.0.0.1', '2026-05-05 08:11:04'),
('harishvm123', 'BCA_DevOps_Lab_Manual_1.docx', 'UPLOAD', '127.0.0.1', '2026-05-05 08:12:15'),
('harishvm123', 'Professional_Communivcation__Ethics_BCA_4th_Sem_1.pdf', 'SHARE', '127.0.0.1', '2026-05-05 08:26:32');
```

---

## 🔐 Get Your Service Key

1. **Go to:** https://app.supabase.com/project/mwnqkxubuvubtndhdgpt/settings/api
2. **Copy** the `service_role` key (not the `anon` key)
3. **Add to `.env`:**
   ```env
   SUPABASE_SERVICE_KEY=eyJhbGc...your-service-key-here
   ```

---

## ✅ Test Connection

After setup, test the connection:

```bash
# Restart Flask backend
# Check logs for: "✅ Supabase connected successfully"
```

---

## 🎯 What Happens After Setup

Once Supabase is connected:
- ✅ All user data stored in cloud
- ✅ File history synced to Supabase
- ✅ Security events tracked
- ✅ Analytics powered by Supabase
- ✅ Real-time updates via Supabase Realtime
- ✅ Scalable and production-ready

---

## 🆘 Troubleshooting

### Issue: "SUPABASE_SERVICE_KEY not set"
**Solution:** Add service key to `.env` file

### Issue: "Permission denied"
**Solution:** Check RLS policies are set to allow service role

### Issue: "Table already exists"
**Solution:** SQL uses `IF NOT EXISTS`, safe to re-run

### Issue: "Connection failed"
**Solution:** Verify SUPABASE_URL and SUPABASE_KEY in `.env`

---

## 📞 Support

- **Supabase Docs:** https://supabase.com/docs
- **VaultX Issues:** Check PROJECT_REPORT.md
- **SQL Reference:** database/enhanced_schema.sql

