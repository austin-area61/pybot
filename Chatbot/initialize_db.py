import sqlite3

# Connect to the database
conn = sqlite3.connect('chatbot.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    preference TEXT
)
''')

conn.commit()
conn.close()

print("Database initialized.")
