-- Import history data to file_history table
INSERT INTO file_history (username, filename, action, ip_address, created_at) VALUES
('harishvm123', NULL, 'LOGIN', '127.0.0.1', '2026-05-05 08:11:04'),
('harishvm123', 'BCA_DevOps_Lab_Manual_1.docx', 'UPLOAD', '127.0.0.1', '2026-05-05 08:12:15'),
('harishvm123', 'Professional_Communivcation__Ethics_BCA_4th_Sem_1.pdf', 'SHARE', '127.0.0.1', '2026-05-05 08:26:32');

-- Note: Users table requires password hashes
-- You'll need to reset passwords after creating accounts in Supabase
-- Or use Supabase Auth for user management instead of direct table inserts
