import sqlite3
import pandas as pd

def db_query_date(item, min_date, max_date):
    """Queries the database for an item between a date range
    
    Keyword arguments:
    item = item number to be queried
    min_date = lower bound for date range
    max_date = upper bound for date range"""
    
    # Connect to SQLite database
    conn = sqlite3.connect(r'C:\Users\Affco\SQLite\sqlite-tools-win32-x86-3420000\invoice_db.db')

    # Query data into a pandas DataFrame, convert datatype and limit data
    df = pd.read_sql_query("SELECT * FROM invoices", conn)
    df['SELL BY'] = pd.to_datetime(df['SELL BY'])
    df = df[(df['ITEM'] == item) & (df['SELL BY'] >= min_date) & (df['SELL BY'] <= max_date)]
    df = df.sort_values(by=['SELL BY'])

    # Show the DataFrame & export
    print(df)
    df.to_csv('C:/Users/Affco/Desktop/data.csv')

    # Don't forget to close the connection
    conn.close()


def db_query_invoices():
    """Sums total net weight for each delivery"""

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
    """exports list of negative dollar amount invoices"""

    conn = sqlite3.connect(r'C:\Users\Affco\SQLite\sqlite-tools-win32-x86-3420000\invoice_db.db')

    query = '''SELECT * FROM invoices WHERE PRICE < 0'''
    df = pd.read_sql_query(query, conn)
    print(df)
    df.to_csv('C:/Users/Affco/Desktop/credits.csv')

    conn.close()