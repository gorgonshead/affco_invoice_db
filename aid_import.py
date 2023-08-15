import os
import sqlite3
import pandas as pd
from tkinter import *
from aid_import_def import *

def create_table(conn):
    cursor = conn.cursor()

    create_table_invoices_sql = """
    CREATE TABLE IF NOT EXISTS invoices (
    CUSTOMER INTEGER,
    'ORDER' INTEGER,
    DELIVERY INTEGER,
    PALLET TEXT,
    ITEM INTEGER,
    DESCRIPTION TEXT,
    `SELL BY` TIMESTAMP,
    CW TEXT,
    QUANTITY INTEGER,
    UOM TEXT,
    `GW LINE ITEM` REAL,
    `BOX TARE` REAL,
    `GW PRODUCT` REAL,
    `PACKAGE TARE` REAL,
    `NW PRODUCT` REAL,
    PRICE REAL,
    CWF TEXT,
    PUOM TEXT
    );
    """

    create_table_delivery_date_sql = """
    CREATE TABLE IF NOT EXISTS delivery_date (
    Delivery_Date TEXT,
    Delivery_Number REAL
    );
    """

    cursor.execute(create_table_invoices_sql)
    cursor.execute(create_table_delivery_date_sql)

def aid_import(treeview, root, conn):
    # Initialize variables for con, import files, & desktop path 
    create_table(conn)
    paths = select_files()
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

    # Initialize most recent sell bys
    last_sellbys = pd.read_sql_query('SELECT ITEM, MAX("SELL BY") as "SELL BY" FROM invoices GROUP BY ITEM', conn)
    last_sellbys['SELL BY'] = pd.to_datetime(last_sellbys['SELL BY'], errors='coerce')

    # Loop through every chosen file
    for path in paths:

        # Check if the file is a CSV
        if path.endswith('.csv'):

            # Load the CSV file into a pandas DataFrame
            df = pd.read_csv(path, encoding='ISO-8859-1', parse_dates=['SELL BY'])

            #check for bad sell bys
            bad_sh_date_chk(conn, last_sellbys, desktop_path, df, root)

            #check for matching headers
            header_check(conn, path)

            # Run check if invoice numbers are already in db
            df = dup_inv(conn, df)

            # Prompt for delivery date, then add date/invoice number to correct table
            deliv_date(conn, df, root)

            if df.empty:

                duplicate_er = tk.Toplevel(root)
                label = Label(duplicate_er, text="This invoice has been imported.")
                label.pack(padx=10, pady=10)
                button = Button(duplicate_er, text="OK", command=duplicate_er.destroy)
                button.pack(padx=10, pady=10, side=BOTTOM)
                
                return
            else:
 
                # Add df to the treeview widget
                add_treeview(df, treeview)             

                # Convert the DataFrame into a SQLite table
                df.to_sql(name='invoices', con=conn, if_exists='append', index=False)

        else:
            print('Please upload a .csv file')