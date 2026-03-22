import sqlite3
conn = sqlite3.connect('backend/instance/langlocaljobs.db')
c = conn.cursor()

# 1. Get the schema of the current profiles table
c.execute("PRAGMA table_info(profiles)")
columns = c.fetchall()
print('Current columns:', [col[1] for col in columns])

# 2. Create a new table without user_id
c.execute('''
CREATE TABLE IF NOT EXISTS profiles_new (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(50) DEFAULT 'user',
    FOREIGN KEY(id) REFERENCES users(id)
)
''')

# 3. Copy data from old table to new table (excluding user_id)
c.execute('''
INSERT INTO profiles_new (id, name, role)
SELECT id, name, role FROM profiles
''')

# 4. Drop the old profiles table
c.execute('DROP TABLE profiles')

# 5. Rename the new table to profiles
c.execute('ALTER TABLE profiles_new RENAME TO profiles')

conn.commit()
conn.close()
print('profiles table fixed: user_id column removed.')
