import sqlite3
import pandas as pd
import os
from datetime import datetime
import babel.numbers

def connection():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'invoice_db.db')
    print(db_path)
    return sqlite3.connect(db_path)

def desktop_path():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    return desktop_path

def db_query_date(item, min_date, max_date, conn):
    """Queries the database for an item between a date range
    
    Keyword arguments:\n
      item = item number to be queried\n
      min_date = lower bound for date range\n
      max_date = upper bound for date range\n
      conn = connection object to db"""
    
    min_date = pd.to_datetime(min_date, format="%m/%d/%y").date()
    max_date = pd.to_datetime(max_date, format="%m/%d/%y").date()

    # Query data into a pandas DataFrame, convert datatype and limit data
    df = pd.read_sql_query("SELECT * FROM invoices", conn)
    df['SELL BY'] = pd.to_datetime(df['SELL BY'], errors='coerce').dt.date
    df['QUANTITY'] = df['QUANTITY'].astype(int)
    df['ITEM'] = df['ITEM'].astype(str)
    df = df[(df['ITEM'] == item) & df['SELL BY'].between(min_date, max_date)]
    df = df.sort_values(by=['SELL BY'])

    return df

def db_query_invoices():
    """Sums total net weight for each delivery"""

    conn = connection()
    
    query = '''
    SELECT invoices.DELIVERY, SUM(invoices."NW PRODUCT"), delivery_date.delivery_date 
    FROM invoices 
    LEFT JOIN delivery_date 
    ON invoices.DELIVERY = delivery_date.delivery_number
    GROUP BY invoices.DELIVERY
    '''

    df = pd.read_sql_query(query, conn)
    print(df)

def db_query_credits():
    """exports list of negative dollar amount invoices"""

    conn = connection()

    query = '''SELECT * FROM invoices WHERE PRICE < 0'''
    df = pd.read_sql_query(query, conn)
    print(df)
    df.to_csv('C:/Users/Affco/Desktop/credits.csv')