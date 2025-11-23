import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect("database.db")
c = conn.cursor()

# Create table
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

# Insert TEACHER account
username = "teacher1"
password = generate_password_hash("1234")
role = "teacher"

try:
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
              (username, password, role))
    print("Teacher account created!")
except:
    print("Teacher already exists.")

conn.commit()
conn.close()
print("Database Setup Completed!")