import sqlite3
import csv

# Export transfers.db history table
print("Exporting transfers.db -> history table...")
conn = sqlite3.connect('transfers.db')
cur = conn.cursor()

# Get column names
cur.execute('PRAGMA table_info(history)')
columns = [col[1] for col in cur.fetchall()]

# Get all data
cur.execute('SELECT * FROM history')
rows = cur.fetchall()

# Write to CSV
with open('history_export.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(columns)
    writer.writerows(rows)

print(f"✅ Exported {len(rows)} rows to history_export.csv")
print(f"   Columns: {', '.join(columns)}")
conn.close()

# Export users.db users table
print("\nExporting users.db -> users table...")
conn = sqlite3.connect('users.db')
cur = conn.cursor()

# Get column names
cur.execute('PRAGMA table_info(users)')
columns = [col[1] for col in cur.fetchall()]

# Get all data (excluding password for security)
cur.execute('SELECT id, username, email FROM users')
rows = cur.fetchall()

# Write to CSV
with open('users_export.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'username', 'email'])
    writer.writerows(rows)

print(f"✅ Exported {len(rows)} users to users_export.csv")
print(f"   Columns: id, username, email (password excluded for security)")
conn.close()

print("\n📁 Files created:")
print("   - history_export.csv")
print("   - users_export.csv")
