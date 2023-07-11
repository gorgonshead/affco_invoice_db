import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect(r'C:\Users\Affco\SQLite\sqlite-tools-win32-x86-3420000\invoice_db.db')

# Query data into a pandas DataFrame
df = pd.read_sql_query("SELECT * FROM invoices", conn)

df['SELL BY'] = pd.to_datetime(df['SELL BY'])

df = df['DELIVERY'].max()

df

# Show the DataFrame
print(df)

# Don't forget to close the connection
conn.close()