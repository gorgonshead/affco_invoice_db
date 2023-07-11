import sqlite3
import pandas as pd

def db_query_date(item, sell_by):
    # Connect to SQLite database
    conn = sqlite3.connect(r'C:\Users\Affco\SQLite\sqlite-tools-win32-x86-3420000\invoice_db.db')

    # Query data into a pandas DataFrame, convert datatype and limit data
    df = pd.read_sql_query("SELECT * FROM invoices", conn)
    df['SELL BY'] = pd.to_datetime(df['SELL BY'])
    df = df[(df['ITEM'] == item) & (df['SELL BY'] > sell_by)]
    df = df.sort_values(by=['SELL BY'])

    # Show the DataFrame & export
    print(df)
    df.to_csv('C:/Users/Affco/Desktop/data.csv')

    # Don't forget to close the connection
    conn.close()

def db_query_invoices():
    conn = sqlite3.connect(r'C:\Users\Affco\SQLite\sqlite-tools-win32-x86-3420000\invoice_db.db')
    
    query = '''
    SELECT invoices.DELIVERY, SUM(invoices."NW PRODUCT"), delivery_date.delivery_date 
    FROM invoices 
    LEFT JOIN delivery_date 
    ON invoices.DELIVERY = delivery_date.delivery_number
    GROUP BY invoices.DELIVERY
    '''

    df = pd.read_sql_query(query, conn)
    print(df)
    df.to_csv('C:/Users/Affco/Desktop/data.csv')

    conn.close()

def db_query_credits():
    conn = sqlite3.connect(r'C:\Users\Affco\SQLite\sqlite-tools-win32-x86-3420000\invoice_db.db')

    query = '''SELECT * FROM invoices WHERE PRICE < 0'''
    df = pd.read_sql_query(query, conn)
    print(df)
    df.to_csv('C:/Users/Affco/Desktop/credits.csv')

    conn.close()