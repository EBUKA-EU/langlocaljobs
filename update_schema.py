import sqlite3
conn = sqlite3.connect('backend/instance/langlocaljobs.db')
c = conn.cursor()

# Add updated_at and role to profiles if not present
c.execute("PRAGMA table_info(profiles)")
profile_cols = [col[1] for col in c.fetchall()]
if 'updated_at' not in profile_cols:
    c.execute("ALTER TABLE profiles ADD COLUMN updated_at DATETIME")
if 'role' not in profile_cols:
    c.execute("ALTER TABLE profiles ADD COLUMN role VARCHAR(50) DEFAULT 'user'")

# Add last_logged_in to users if not present
c.execute("PRAGMA table_info(users)")
user_cols = [col[1] for col in c.fetchall()]
if 'last_logged_in' not in user_cols:
    c.execute("ALTER TABLE users ADD COLUMN last_logged_in DATETIME")

conn.commit()
conn.close()
print('Schema updated: profiles (updated_at, role), users (last_logged_in)')
