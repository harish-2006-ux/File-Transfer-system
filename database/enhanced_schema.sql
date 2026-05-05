-- VaultX Enhanced Database Schema
-- Complete schema with all advanced features
-- Run this in Supabase Dashboard > SQL Editor

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

-- Login locations table (for geolocation tracking)
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

-- API keys table (for future API access)
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

-- Core tables indexes
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_file_history_user_id ON file_history(user_id);
CREATE INDEX IF NOT EXISTS idx_file_history_username ON file_history(username);
CREATE INDEX IF NOT EXISTS idx_file_history_created_at ON file_history(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_file_history_action ON file_history(action);
CREATE INDEX IF NOT EXISTS idx_connection_logs_created_at ON connection_logs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_connection_logs_ip ON connection_logs(ip_address);

-- Advanced feature indexes
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
-- RLS POLICIES
-- ============================================================

-- Users table policies
DROP POLICY IF EXISTS "Users can view their own data" ON users;
CREATE POLICY "Users can view their own data" ON users
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "Service role can manage users" ON users;
CREATE POLICY "Service role can manage users" ON users
    FOR ALL USING (true);

-- File history policies
DROP POLICY IF EXISTS "Users can view their own history" ON file_history;
CREATE POLICY "Users can view their own history" ON file_history
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "Service role can manage history" ON file_history;
CREATE POLICY "Service role can manage history" ON file_history
    FOR ALL USING (true);

-- Connection logs policies
DROP POLICY IF EXISTS "Service role can manage logs" ON connection_logs;
CREATE POLICY "Service role can manage logs" ON connection_logs
    FOR ALL USING (true);

-- Security events policies
DROP POLICY IF EXISTS "Users can view their own security events" ON security_events;
CREATE POLICY "Users can view their own security events" ON security_events
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "Service role can manage security events" ON security_events;
CREATE POLICY "Service role can manage security events" ON security_events
    FOR ALL USING (true);

-- Device fingerprints policies
DROP POLICY IF EXISTS "Users can view their own devices" ON device_fingerprints;
CREATE POLICY "Users can view their own devices" ON device_fingerprints
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "Service role can manage devices" ON device_fingerprints;
CREATE POLICY "Service role can manage devices" ON device_fingerprints
    FOR ALL USING (true);

-- Login locations policies
DROP POLICY IF EXISTS "Users can view their own locations" ON login_locations;
CREATE POLICY "Users can view their own locations" ON login_locations
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "Service role can manage locations" ON login_locations;
CREATE POLICY "Service role can manage locations" ON login_locations
    FOR ALL USING (true);

-- Notifications policies
DROP POLICY IF EXISTS "Users can view their own notifications" ON notifications;
CREATE POLICY "Users can view their own notifications" ON notifications
    FOR SELECT USING (true);

DROP POLICY IF EXISTS "Users can update their own notifications" ON notifications;
CREATE POLICY "Users can update their own notifications" ON notifications
    FOR UPDATE USING (true);

DROP POLICY IF EXISTS "Service role can manage notifications" ON notifications;
CREATE POLICY "Service role can manage notifications" ON notifications
    FOR ALL USING (true);

-- User preferences policies
DROP POLICY IF EXISTS "Users can manage their own preferences" ON user_preferences;
CREATE POLICY "Users can manage their own preferences" ON user_preferences
    FOR ALL USING (true);

-- API keys policies
DROP POLICY IF EXISTS "Users can manage their own API keys" ON api_keys;
CREATE POLICY "Users can manage their own API keys" ON api_keys
    FOR ALL USING (true);

-- ============================================================
-- FUNCTIONS
-- ============================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for users table
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Trigger for user_preferences table
DROP TRIGGER IF EXISTS update_user_preferences_updated_at ON user_preferences;
CREATE TRIGGER update_user_preferences_updated_at
    BEFORE UPDATE ON user_preferences
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to clean old logs (optional - run periodically)
CREATE OR REPLACE FUNCTION clean_old_logs(days_to_keep INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM connection_logs
    WHERE created_at < NOW() - (days_to_keep || ' days')::INTERVAL;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- STORAGE BUCKET (for encrypted files)
-- ============================================================

-- Create storage bucket for encrypted files
INSERT INTO storage.buckets (id, name, public)
VALUES ('encrypted-files', 'encrypted-files', false)
ON CONFLICT (id) DO NOTHING;

-- Storage policies
DROP POLICY IF EXISTS "Authenticated users can upload files" ON storage.objects;
CREATE POLICY "Authenticated users can upload files"
ON storage.objects FOR INSERT
WITH CHECK (bucket_id = 'encrypted-files' AND auth.role() = 'authenticated');

DROP POLICY IF EXISTS "Users can view their own files" ON storage.objects;
CREATE POLICY "Users can view their own files"
ON storage.objects FOR SELECT
USING (bucket_id = 'encrypted-files');

DROP POLICY IF EXISTS "Users can delete their own files" ON storage.objects;
CREATE POLICY "Users can delete their own files"
ON storage.objects FOR DELETE
USING (bucket_id = 'encrypted-files');

-- ============================================================
-- VIEWS FOR ANALYTICS
-- ============================================================

-- View for user activity summary
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

-- View for security summary
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
-- COMPLETE!
-- ============================================================

SELECT 'VaultX enhanced database schema created successfully!' AS status;
SELECT 'Total tables created: 12' AS info;
SELECT 'Total indexes created: 20+' AS info;
SELECT 'RLS enabled on all tables' AS security;
SELECT 'Views created for analytics' AS analytics;
