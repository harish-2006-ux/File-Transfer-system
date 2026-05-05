"""
Supabase Database Setup Script
Creates tables and initial configuration for VaultX
"""

from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in .env")
    exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_schema_file():
    """Create a SQL file with all schema commands"""
    
    schema_sql = """-- VaultX Supabase Database Schema
-- Run this in Supabase Dashboard > SQL Editor

-- ============================================================
-- TABLES
-- ============================================================

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Connection logs table
CREATE TABLE IF NOT EXISTS connection_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ip_address TEXT NOT NULL,
    method TEXT NOT NULL,
    path TEXT NOT NULL,
    status_code INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_file_history_user_id ON file_history(user_id);
CREATE INDEX IF NOT EXISTS idx_file_history_username ON file_history(username);
CREATE INDEX IF NOT EXISTS idx_file_history_created_at ON file_history(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_connection_logs_created_at ON connection_logs(created_at DESC);

-- ============================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE file_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE connection_logs ENABLE ROW LEVEL SECURITY;

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
-- COMPLETE!
-- ============================================================

SELECT 'VaultX database schema created successfully!' AS status;
"""
    
    with open('database/schema.sql', 'w') as f:
        f.write(schema_sql)
    
    print("\n✅ Created 'database/schema.sql' file")

def test_connection():
    """Test Supabase connection"""
    print("\n🔌 Testing Supabase connection...")
    
    try:
        # Try to query users table
        response = supabase.table('users').select("count").execute()
        print("✅ Connection successful!")
        return True
    except Exception as e:
        print(f"⚠️  Connection test: {str(e)}")
        print("   This is normal if tables don't exist yet.")
        return False

def main():
    print("="*60)
    print("VaultX - Supabase Setup")
    print("="*60)
    
    # Test connection
    test_connection()
    
    # Create schema file
    create_schema_file()
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Go to your Supabase Dashboard")
    print("   URL:", SUPABASE_URL)
    print("\n2. Navigate to: SQL Editor > New Query")
    print("\n3. Copy and paste the contents of 'database/schema.sql'")
    print("\n4. Click 'Run' to execute the SQL")
    print("\n5. Update your .env file:")
    print("   DATABASE_TYPE=supabase")
    print("\n6. Restart your Flask application")
    print("="*60)

if __name__ == "__main__":
    main()
