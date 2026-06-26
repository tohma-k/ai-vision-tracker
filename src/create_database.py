import sqlite3

DB_NAME = "faces.gb"

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS faces (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    encoding BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

connection.commit()
connection.close()

print("Database created successfully.")