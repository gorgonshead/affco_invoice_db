import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'invoice_db.db')
conn = sqlite3.connect(db_path)

# Print all tables in the database
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

conn.close()