import os
import sqlite3
import pandas as pd
import csv
import sys

def bad_sh_date_chk(conn, last_sellbys, desktop_path, df, cnt):
    """Export sell by dates older than the best dates for that item.
    
    Keyword arguments:
    conn = database connection object
    last_sellbys = pandas dataframe that contains a list of dates
    desktop_path = path to the current user's desktop
    df = pandas dataframe to check last_sellbys against"""

    # Merge the last_sellbys on the db df
    # If the best sellbys in db are greater than incoming, print &
    # export to desktop
    merged_df = pd.merge(df, last_sellbys, on='ITEM', how='inner', suffixes=('', '_in_db'))
    earlier_dates = merged_df[merged_df['SELL BY'] < merged_df['SELL BY_in_db']]
    if not earlier_dates.empty:
        print('Incoming dates earlier than those in the database:')
        print(earlier_dates[['ITEM', 'SELL BY', 'QUANTITY', 'SELL BY_in_db']])
        earlier_dates.to_csv(os.path.join(desktop_path, f'sell_bys{cnt}.csv'))
    else:
        print('All dates better than previous invoices.')

def dup_inv(conn, df):
    """Check a list of all delivery numbers against incoming delivery numbers, return empty if matches"""

    # Select all delivery invoice nubmers
    existing_delivery = pd.read_sql_query('SELECT DISTINCT delivery FROM invoices', conn)['DELIVERY'].values
    
    # Flag invoice numbers that match
    # Drop flagged invoice numbers
    df['flag'] = df['DELIVERY'].isin(existing_delivery)
    df = df[~df['flag']]
    df = df.drop(columns=['flag'])
    print(df)
    return df

def header_check(conn, path):
    """Compare headers from .csv to columns in db, raise exception if !match"""

    # Get column names from database
    cursor = conn.cursor()
    table_info = cursor.execute(f"PRAGMA table_info({'invoices'})").fetchall()
    column_names = [info[1] for info in table_info]

    # Get headers from .cvs
    with open(path, newline='') as f:
        reader = csv.reader(f)
        csv_headers = next(reader)
    
    # Compare headers, then if don't match stop program
    if set(csv_headers) == set(column_names):
        print('.csv headers match')
    else:
        raise Exception('File headers do not match.')