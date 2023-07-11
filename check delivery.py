import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('invoice_db.db')

# Query data into a pandas DataFrame
df = pd.read_sql_query('SELECT * FROM delivery_date', conn)

df['Delivery_Date'] = pd.to_datetime(df['Delivery_Date'])

df = df.sort_values(by=['Delivery_Date'])

# Show the DataFrame
print(df)

# Don't forget to close the connection
conn.close()