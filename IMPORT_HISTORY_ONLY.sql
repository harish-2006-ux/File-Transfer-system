-- ============================================================
-- Import File History Only (Recommended)
-- Run this in: Supabase Dashboard > SQL Editor
-- ============================================================

-- This imports only file history.
-- Users should sign up fresh via the VaultX application.
-- This is the RECOMMENDED approach for security.

-- Import file history
INSERT INTO file_history (username, filename, action, ip_address, created_at) VALUES
('harishvm123', NULL, 'LOGIN', '127.0.0.1', '2026-05-05 08:11:04'),
('harishvm123', 'BCA_DevOps_Lab_Manual_1.docx', 'UPLOAD', '127.0.0.1', '2026-05-05 08:12:15'),
('harishvm123', 'Professional_Communivcation__Ethics_BCA_4th_Sem_1.pdf', 'SHARE', '127.0.0.1', '2026-05-05 08:26:32');

-- Verify import
SELECT 'File history imported successfully!' AS status;
SELECT COUNT(*) AS history_count FROM file_history;

-- Display imported history
SELECT username, filename, action, ip_address, created_at 
FROM file_history 
ORDER BY created_at DESC;

-- ============================================================
-- NEXT STEPS:
-- ============================================================
-- 1. Go to http://127.0.0.1:8000
-- 2. Sign up with username: harishvm123
-- 3. Use email: hhareeshvm@gmail.com
-- 4. Create a new password
-- 5. The file history will be linked automatically
-- ============================================================
