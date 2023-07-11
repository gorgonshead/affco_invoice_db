import os
import sqlite3
import pandas as pd

# Specify the directory you want to use
directory = r"C:\Users\Affco\Desktop\Database Stuff\Put New Stuff Here"

# Create a connection to the SQLite database
# (If the database does not exist, it will be created)
conn = sqlite3.connect(r'C:\Users\Affco\SQLite\sqlite-tools-win32-x86-3420000\invoice_db.db')

#query invoice_db for unique order numbers & sell bys
existing_delivery = pd.read_sql_query('SELECT DISTINCT delivery FROM invoices', conn)['DELIVERY'].values
last_sellbys = pd.read_sql_query('SELECT ITEM, MAX("SELL BY") as "SELL BY" FROM invoices GROUP BY ITEM', conn)
last_sellbys['SELL BY'] = pd.to_datetime(last_sellbys['SELL BY'])

# Loop through every file in the directory
for filename in os.listdir(directory):

    # Check if the file is a CSV
    if filename.endswith('.csv') and filename != "New Invoices.csv":
        
        # Construct the full file path
        path = os.path.join(directory, filename)
        
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(path, encoding='ISO-8859-1', parse_dates=['SELL BY'])

        #check DELIVERY for newer dates in invoices, then export
        merged_df = pd.merge(df, last_sellbys, on='ITEM', how='inner', suffixes=('', '_in_db'))
        earlier_dates = merged_df[merged_df['SELL BY'] < merged_df['SELL BY_in_db']]

        if not earlier_dates.empty:
            print('Incoming dates earlier than those in the database:')
            print(earlier_dates[['ITEM', 'SELL BY', 'QUANTITY', 'SELL BY_in_db']])
            earlier_dates.to_csv('C:/Users/Affco/Desktop/sell_by.csv')

        #check unique order numbers for 
        df['flag'] = df['DELIVERY'].isin(existing_delivery)
        df = df[~df['flag']]
        df = df.drop(columns=['flag'])
        
        # Convert the DataFrame into a SQLite table
        df.to_sql(name='invoices', con=conn, if_exists='append', index=False)

        print(df)

# Close the connection to the SQLite database
conn.close()