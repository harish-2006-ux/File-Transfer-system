-- ============================================================
-- Import Users to Supabase
-- Run this in: Supabase Dashboard > SQL Editor
-- ============================================================

-- Note: These are temporary passwords. Users should reset them after first login.
-- Password format: bcrypt hash of "TempPassword123!"

-- Import users with temporary hashed passwords
INSERT INTO users (username, email, password, created_at) VALUES
(
    'testuser', 
    'test@example.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxKzQWu4W',  -- TempPassword123!
    NOW()
),
(
    'hhareeshvm@gmail.com', 
    'hhareeshvm@gmail.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxKzQWu4W',  -- TempPassword123!
    NOW()
),
(
    'harishvm123', 
    'hhareeshvm@gmail.com', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYIxKzQWu4W',  -- TempPassword123!
    NOW()
)
ON CONFLICT (username) DO NOTHING;

-- Import file history
INSERT INTO file_history (username, filename, action, ip_address, created_at) VALUES
('harishvm123', NULL, 'LOGIN', '127.0.0.1', '2026-05-05 08:11:04'),
('harishvm123', 'BCA_DevOps_Lab_Manual_1.docx', 'UPLOAD', '127.0.0.1', '2026-05-05 08:12:15'),
('harishvm123', 'Professional_Communivcation__Ethics_BCA_4th_Sem_1.pdf', 'SHARE', '127.0.0.1', '2026-05-05 08:26:32');

-- Verify imports
SELECT 'Users imported successfully!' AS status;
SELECT COUNT(*) AS user_count FROM users;
SELECT COUNT(*) AS history_count FROM file_history;

-- Display imported users (without passwords)
SELECT username, email, created_at FROM users ORDER BY created_at DESC;

-- Display imported history
SELECT username, filename, action, ip_address, created_at FROM file_history ORDER BY created_at DESC;

-- ============================================================
-- IMPORTANT NOTES:
-- ============================================================
-- 1. All users have temporary password: TempPassword123!
-- 2. Users should change password after first login
-- 3. Or better: Have users sign up fresh via the VaultX app
-- ============================================================
