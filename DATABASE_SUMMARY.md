# 📊 VaultX Database Summary

## 🗄️ Total Tables: 9 Tables

### Core Tables (3)

#### 1. **users**
- **Purpose:** User accounts and authentication
- **Columns:** id, username, email, password, last_login_ip, last_login_at, last_user_agent, created_at, updated_at
- **CSV File:** `users_supabase.csv` (3 users)
- **Data:**
  - testuser (test@example.com)
  - hhareeshvm@gmail.com
  - harishvm123 (hhareeshvm@gmail.com)

#### 2. **file_history**
- **Purpose:** Track all file operations (upload, download, share, delete)
- **Columns:** id, user_id, username, filename, action, ip_address, user_agent, filesize, created_at
- **CSV File:** `file_history_supabase.csv` (3 records)
- **Data:**
  - LOGIN by harishvm123
  - UPLOAD: BCA_DevOps_Lab_Manual_1.docx
  - SHARE: Professional_Communivcation__Ethics_BCA_4th_Sem_1.pdf

#### 3. **connection_logs**
- **Purpose:** HTTP request logging for monitoring
- **Columns:** id, ip_address, method, path, status_code, user_agent, response_time, created_at
- **CSV File:** None (auto-populated)

---

### Advanced Feature Tables (6)

#### 4. **security_events**
- **Purpose:** Track security alerts and suspicious activity
- **Columns:** id, user_id, username, event_type, ip_address, user_agent, details (JSONB), severity, created_at
- **CSV File:** None (auto-populated)
- **Event Types:** SUSPICIOUS_LOGIN, FAILED_LOGIN, PASSWORD_CHANGE, etc.

#### 5. **device_fingerprints**
- **Purpose:** Track and trust user devices
- **Columns:** id, user_id, fingerprint_hash, device_name, browser, os, last_seen_at, is_trusted, created_at
- **CSV File:** None (auto-populated)

#### 6. **login_locations**
- **Purpose:** Geolocation tracking for logins
- **Columns:** id, user_id, ip_address, country, city, region, latitude, longitude, timezone, login_count, last_login_at, created_at
- **CSV File:** None (auto-populated)

#### 7. **notifications**
- **Purpose:** In-app notifications for users
- **Columns:** id, user_id, title, message, notification_type, is_read, data (JSONB), created_at
- **CSV File:** None (auto-populated)

#### 8. **user_preferences**
- **Purpose:** User settings and preferences
- **Columns:** id, user_id, email_notifications, login_alerts, suspicious_activity_alerts, daily_summary, theme, language, timezone, created_at, updated_at
- **CSV File:** None (auto-populated with defaults)

#### 9. **api_keys**
- **Purpose:** API access tokens for programmatic access
- **Columns:** id, user_id, key_hash, name, permissions (JSONB), last_used_at, expires_at, is_active, created_at
- **CSV File:** None (created on demand)

---

## 📁 CSV Files: 4 Files

### 1. **file_history_supabase.csv** (281 bytes)
```csv
username,filename,action,ip_address,created_at
harishvm123,-,LOGIN,127.0.0.1,2026-05-05 08:11:04
harishvm123,BCA_DevOps_Lab_Manual_1.docx,UPLOAD,127.0.0.1,2026-05-05 08:12:15
harishvm123,Professional_Communivcation__Ethics_BCA_4th_Sem_1.pdf,SHARE,127.0.0.1,2026-05-05 08:26:32
```
- **Purpose:** Import file history into Supabase
- **Records:** 3
- **Ready for:** Direct import to `file_history` table

### 2. **users_supabase.csv** (120 bytes)
```csv
username,email
testuser,test@example.com
hhareeshvm@gmail.com,hhareeshvm@gmail.com
harishvm123,hhareeshvm@gmail.com
```
- **Purpose:** Import users into Supabase
- **Records:** 3
- **Note:** Passwords need to be reset after import

### 3. **history_export.csv** (281 bytes)
```csv
id,username,filename,action,ip,timestamp
1,harishvm123,-,LOGIN,127.0.0.1,2026-05-05 08:11:04
2,harishvm123,BCA_DevOps_Lab_Manual_1.docx,UPLOAD,127.0.0.1,2026-05-05 08:12:15
3,harishvm123,Professional_Communivcation__Ethics_BCA_4th_Sem_1.pdf,SHARE,127.0.0.1,2026-05-05 08:26:32
```
- **Purpose:** SQLite export (old format)
- **Records:** 3
- **Note:** Use `file_history_supabase.csv` instead for Supabase

### 4. **users_export.csv** (129 bytes)
```csv
id,username,email
1,testuser,test@example.com
2,hhareeshvm@gmail.com,hhareeshvm@gmail.com
3,harishvm123,hhareeshvm@gmail.com
```
- **Purpose:** SQLite export (old format)
- **Records:** 3
- **Note:** Use `users_supabase.csv` instead for Supabase

---

## 📊 Database Statistics

### Tables by Category:
- **Core Tables:** 3 (33%)
- **Advanced Features:** 6 (67%)
- **Total:** 9 tables

### CSV Files by Status:
- **Supabase-Ready:** 2 files (`*_supabase.csv`)
- **SQLite Export:** 2 files (`*_export.csv`)
- **Total:** 4 files

### Data Records:
- **Users:** 3 accounts
- **File History:** 3 actions
- **Total Records:** 6

---

## 🔄 Import to Supabase

### Method 1: Using Supabase Dashboard (Recommended)

#### Import Users:
1. Go to: https://app.supabase.com/project/mwnqkxubuvubtndhdgpt/editor
2. Click on `users` table
3. Click "Insert" → "Import data from CSV"
4. Upload: `users_supabase.csv`
5. Map columns: username → username, email → email
6. **Note:** You'll need to set passwords manually or via signup

#### Import File History:
1. Click on `file_history` table
2. Click "Insert" → "Import data from CSV"
3. Upload: `file_history_supabase.csv`
4. Map columns automatically
5. Done!

### Method 2: Using SQL (Faster)

Run this in Supabase SQL Editor:

```sql
-- Import file history
INSERT INTO file_history (username, filename, action, ip_address, created_at) VALUES
('harishvm123', NULL, 'LOGIN', '127.0.0.1', '2026-05-05 08:11:04'),
('harishvm123', 'BCA_DevOps_Lab_Manual_1.docx', 'UPLOAD', '127.0.0.1', '2026-05-05 08:12:15'),
('harishvm123', 'Professional_Communivcation__Ethics_BCA_4th_Sem_1.pdf', 'SHARE', '127.0.0.1', '2026-05-05 08:26:32');

-- Note: Users require password hashes
-- Better to create users via the VaultX signup page
```

---

## 📈 Additional Features

### Indexes: 20+
- Performance optimization for queries
- Faster searches on username, email, dates
- Efficient filtering by action type

### Row Level Security (RLS):
- Enabled on all 9 tables
- Service role has full access
- Users can only see their own data

### Views: 2
1. **user_activity_summary** - Aggregated user statistics
2. **security_summary** - Security event overview

### Triggers: 2
1. **update_users_updated_at** - Auto-update timestamp
2. **update_user_preferences_updated_at** - Auto-update timestamp

---

## 🎯 Quick Reference

### Tables with CSV Data:
✅ `users` → `users_supabase.csv` (3 records)
✅ `file_history` → `file_history_supabase.csv` (3 records)

### Tables Auto-Populated:
- `connection_logs` (via Flask app)
- `security_events` (via security monitor)
- `device_fingerprints` (on login)
- `login_locations` (on login with geolocation)
- `notifications` (via notification service)
- `user_preferences` (on user creation)
- `api_keys` (on demand)

---

## 📝 Summary

| Item | Count |
|------|-------|
| **Total Tables** | 9 |
| **Core Tables** | 3 |
| **Advanced Tables** | 6 |
| **CSV Files** | 4 |
| **Supabase-Ready CSVs** | 2 |
| **Total Data Records** | 6 |
| **Indexes** | 20+ |
| **Views** | 2 |
| **Triggers** | 2 |

---

## 🚀 Next Steps

1. ✅ **Create Tables** - Run SQL from `SUPABASE_SETUP.md`
2. ✅ **Import Data** - Use CSV files or SQL inserts
3. ✅ **Add Service Key** - Update `.env` file
4. ✅ **Restart Backend** - Connect to Supabase
5. ✅ **Test** - Create user, upload file, check Supabase

---

## 📖 Related Files

- **Schema:** `database/enhanced_schema.sql`
- **Setup Guide:** `SUPABASE_SETUP.md`
- **Import SQL:** `import_to_supabase.sql`
- **CSV Files:** `*_supabase.csv`

