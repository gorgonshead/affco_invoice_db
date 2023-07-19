import os
import sqlite3
import pandas as pd
from tkinter.filedialog import askopenfilenames
from aid_import_def import bad_sh_date_chk, dup_inv, header_check, deliv_date

# Initialize variables for con, import files, & desktop path 
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'invoice_db.db')
conn = sqlite3.connect(db_path)
paths = askopenfilenames()
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Initialize most recent sell bys
last_sellbys = pd.read_sql_query('SELECT ITEM, MAX("SELL BY") as "SELL BY" FROM invoices GROUP BY ITEM', conn)
last_sellbys['SELL BY'] = pd.to_datetime(last_sellbys['SELL BY'])

# Loop through every chosen file
for path in paths:

    # Check if the file is a CSV
    if path.endswith('.csv'):

        cnt = 0
        cnt += 1

        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(path, encoding='ISO-8859-1', parse_dates=['SELL BY'])

        #check for bad sell bys
        bad_sh_date_chk(conn, last_sellbys, desktop_path, df, cnt)

        #check for matching headers
        header_check(conn, path)

        # Run check if invoice numbers are already in db
        df = dup_inv(conn, df)

        # Prompt for delivery date, then add date/invoice number to correct table
        deliv_date(conn, df)

        # Convert the DataFrame into a SQLite table
        df.to_sql(name='invoices', con=conn, if_exists='append', index=False)

    else:
        print('Please upload a .csv file')

# Close the connection to the SQLite database
conn.close()