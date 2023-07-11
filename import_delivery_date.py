import os
import sqlite3
import pandas as pd

# Create a connection to the SQLite database
conn = sqlite3.connect(r'C:\Users\Affco\SQLite\sqlite-tools-win32-x86-3420000\invoice_db.db')

# Retrieve existing 'delivery_number' data
existing_delivery_numbers = pd.read_sql_query('SELECT delivery_number FROM delivery_date', conn)['Delivery_Number'].values

path = r"C:\Users\Affco\Desktop\Database Stuff\Put New Stuff Here\New Invoices.csv"
        
# Load the CSV file into a pandas DataFrame
df = pd.read_csv(path)

# Flag rows where 'delivery_number' is already in the database then drop those
df['flag'] = df['Delivery_Number'].isin(existing_delivery_numbers)
print(df)
df = df[~df['flag']]
df = df.drop(columns=['flag'])
        
# Convert the DataFrame into a SQLite table
df.to_sql(name='delivery_date', con=conn, if_exists='append', index=False)

# Close the connection to the SQLite database
conn.close()