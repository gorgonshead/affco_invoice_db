import os
import sqlite3
import pandas as pd
import tkinter
from tkinter.filedialog import askopenfilenames

# Specify the files you want to use
paths = askopenfilenames()

# Create a path to the desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Create a connection to the SQLite database
# (If the database does not exist, it will be created)
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'invoice_db.db')
conn = sqlite3.connect(db_path)

# query invoice_db for unique order numbers
# query invoice_db for latest sell bys for each item.
existing_delivery = pd.read_sql_query('SELECT DISTINCT delivery FROM invoices', conn)['DELIVERY'].values
last_sellbys = pd.read_sql_query('SELECT ITEM, MAX("SELL BY") as "SELL BY" FROM invoices GROUP BY ITEM', conn)
last_sellbys['SELL BY'] = pd.to_datetime(last_sellbys['SELL BY'])

# Loop through every chosen file
for path in paths:

    # Check if the file is a CSV
    if path.endswith('.csv'):
        
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(path, encoding='ISO-8859-1', parse_dates=['SELL BY'])

        #check DELIVERY for newer dates in invoices
        # Print sell_bys older than the best dates in the database by item
        # Export results to the desktop
        merged_df = pd.merge(df, last_sellbys, on='ITEM', how='inner', suffixes=('', '_in_db'))
        earlier_dates = merged_df[merged_df['SELL BY'] < merged_df['SELL BY_in_db']]
        if not earlier_dates.empty:
            print('Incoming dates earlier than those in the database:')
            print(earlier_dates[['ITEM', 'SELL BY', 'QUANTITY', 'SELL BY_in_db']])
            earlier_dates.to_csv(os.path.join(desktop_path, 'selly_bys.csv'))

        #check unique order numbers for 
        df['flag'] = df['DELIVERY'].isin(existing_delivery)
        df = df[~df['flag']]
        df = df.drop(columns=['flag'])
        
        # Convert the DataFrame into a SQLite table
        df.to_sql(name='invoices', con=conn, if_exists='append', index=False)

        print(df)

# Close the connection to the SQLite database
conn.close()