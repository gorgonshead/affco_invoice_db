import sqlite3
import pandas as pd
import os
from datetime import datetime

def connection():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'invoice_db.db')
    print(db_path)
    return sqlite3.connect(db_path)

def desktop_path():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    return desktop_path

def db_query_date(item, min_date, max_date, conn):
    """Queries the database for an item between a date range
    
    Keyword arguments:
    item = item number to be queried
    min_date = lower bound for date range
    max_date = upper bound for date range"""
    
    min_date = pd.to_datetime(min_date, format="%m/%d/%y")
    max_date = pd.to_datetime(max_date, format="%m/%d/%y")
    print(min_date)
    print(max_date)

    print(type(item))

    # Query data into a pandas DataFrame, convert datatype and limit data
    df = pd.read_sql_query("SELECT * FROM invoices", conn)
    print(df)
    df['SELL BY'] = pd.to_datetime(df['SELL BY'])
    df['ITEM'] = df['ITEM'].astype(str)
    df = df[(df['ITEM'] == item) & df['SELL BY'].between(min_date, max_date)]
    df = df.sort_values(by=['SELL BY'])
    df['SELL BY'] = df['SELL BY'].dt.date

    # Export dataframe
    dkp = desktop_path()
    df.to_csv(os.path.join(dkp, "inv_sell_by.csv"))

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
    
    dkp = desktop_path()
    df.to_csv(os.path.join(dkp, "total_invoices.csv"))

def db_query_credits():
    """exports list of negative dollar amount invoices"""

    conn = connection()

    query = '''SELECT * FROM invoices WHERE PRICE < 0'''
    df = pd.read_sql_query(query, conn)
    print(df)
    df.to_csv('C:/Users/Affco/Desktop/credits.csv')