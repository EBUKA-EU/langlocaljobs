import sqlite3

# Path to your SQLite database
DB_PATH = 'backend/instance/langlocaljobs.db'


def recreate_profiles_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Drop the table if it exists
    c.execute('DROP TABLE IF EXISTS profiles')
    # Recreate the table with the correct schema
    c.execute('''
        CREATE TABLE profiles (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100),
            created_at DATETIME,
            role VARCHAR(50) DEFAULT 'user',
            updated_at DATETIME,
            FOREIGN KEY(id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()
    print('profiles table recreated.')


if __name__ == '__main__':
    recreate_profiles_table()
