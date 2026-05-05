import sqlite3
import csv

# Export transfers.db history table with Supabase column names
print("Exporting for Supabase file_history table...")
conn = sqlite3.connect('transfers.db')
cur = conn.cursor()

# Get all data
cur.execute('SELECT username, filename, action, ip, timestamp FROM history')
rows = cur.fetchall()

# Write to CSV with Supabase column names
with open('file_history_supabase.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    # Use Supabase column names
    writer.writerow(['username', 'filename', 'action', 'ip_address', 'created_at'])
    writer.writerows(rows)

print(f"✅ Exported {len(rows)} rows to file_history_supabase.csv")
print(f"   Columns: username, filename, action, ip_address, created_at")
conn.close()

# Export users.db users table
print("\nExporting for Supabase users table...")
conn = sqlite3.connect('users.db')
cur = conn.cursor()

# Get all data (excluding password for security)
cur.execute('SELECT username, email FROM users')
rows = cur.fetchall()

# Write to CSV
with open('users_supabase.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['username', 'email'])
    writer.writerows(rows)

print(f"✅ Exported {len(rows)} users to users_supabase.csv")
print(f"   Columns: username, email")
conn.close()

print("\n📁 Supabase-ready files created:")
print("   - file_history_supabase.csv (ready for file_history table)")
print("   - users_supabase.csv (ready for users table)")
print("\n💡 Import these files directly into Supabase!")
