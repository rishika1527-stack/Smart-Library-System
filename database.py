import sqlite3

connection = sqlite3.connect("library.db")
cursor = connection.cursor()

# Books table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    category TEXT,
    available TEXT,
    due_date TEXT
)
""")

# Contacts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    message TEXT
)
""")

# Seats table
cursor.execute("""
CREATE TABLE IF NOT EXISTS seats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seat_number TEXT,
    status TEXT
)
""")

connection.commit()
connection.close()

print("Database and tables created successfully!")