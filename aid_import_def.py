import os
import pandas as pd
import csv
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import *
from datetime import datetime
from tkinter.filedialog import askopenfilenames


def bad_sh_date_chk(conn, last_sellbys, desktop_path, df, root):
    """Export sell by dates older than the best dates for that item.
    
    Keyword arguments:\n
      conn = database connection object.\n
      last_sellbys = pandas dataframe that contains a list of dates.\n
      desktop_path = path to the current user's desktop.\n
      df = pandas dataframe to check last_sellbys against."""

    # Merge the last_sellbys on the db df
    # If the best sellbys in db are greater than incoming, print &
    # export to desktop
    merged_df = pd.merge(df, last_sellbys, on='ITEM', how='inner', suffixes=('', '_in_db'))
    earlier_dates = merged_df[merged_df['SELL BY'] < merged_df['SELL BY_in_db']]
    if not earlier_dates.empty:

        def early_dates_export(earlier_dates, root):   
            print('Incoming dates earlier than those in the database:')
            print(earlier_dates[['ITEM', 'SELL BY', 'QUANTITY', 'SELL BY_in_db']])
            invoice_num = pd.unique(earlier_dates['DELIVERY'])
            invoice_num = invoice_num[0]
            earlier_dates.to_csv(os.path.join(desktop_path, f'{invoice_num}_sell_by.csv'))
            root.destroy()

        yes_no_root  = Toplevel(root)
        yes_label = Label(yes_no_root, text="Would you like to export the mixed up dates?")
        yes_label.pack(side=TOP, padx=5, pady=5)
        yes_but = Button(yes_no_root, text="yes", command=lambda: early_dates_export(earlier_dates, yes_no_root))
        yes_but.pack(side=LEFT, padx=5, pady=5)
        no_but = Button(yes_no_root, text="No", command=yes_no_root.destroy)
        no_but.pack(side=RIGHT, padx=5, pady=5)

        yes_no_root.grab_set()

        root.wait_window(yes_no_root)

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
        print('File headers match.')
    else:
        raise Exception('File headers do not match.')
    
def deliv_date(conn, df, root):
    """Query user for the date of delivery, then append date & delivery number to delivery_date table
    
    Keyword arguments:
    conn = connection to database.
    df = dataframe of incoming invoice"""

    if df.empty:
        print("No data to process.")
        return
    
    # Take delivery number from df
    new_invoice = df['DELIVERY'].max()

    # Prompt user for the delivery date, transform to datetime
    new_date = deldate_cal_win(df, root)
    new_date = pd.to_datetime(new_date)
    
    # Get a list of all delivery numbers from the database
    existing_del_num = pd.read_sql_query('SELECT delivery_number FROM delivery_date', conn)['Delivery_Number'].values
    
    # If new_invoice doesn't exist in existing_del_num 
    if new_invoice not in existing_del_num:
        # Create new df and append to the database
        new_df = pd.DataFrame({'Delivery_Date' : [new_date],'Delivery_Number' : [new_invoice]})
        new_df.to_sql(name='delivery_date', con=conn, if_exists='append', index=False)
    else: print(f"The delivery number {new_invoice} already exists in the database.")

def deldate_cal_win(df, root):
    """Create a calendar window to input the delivery date, then return the date selected"""

    def return_date():
        chosen_date.set(new_date_cal.get_date())
        root.destroy()
    
    def invoice_num(df):
        num = df['DELIVERY'].unique()
        return num

    root = tk.Toplevel()
    root.title(f"Delivery date from invoice {invoice_num(df)}")

    mainframe = Frame(root)
    mainframe.pack()

    chosen_date = StringVar()
    choose_date = StringVar(value=datetime.now().strftime('%d/%m/%Y'))
    new_date_cal = Calendar(mainframe, date_pattern='y/mm/dd', textvariable=choose_date)
    new_date_cal.pack()

    button = Button(mainframe, text="OK", command=return_date)
    button.pack(fill=BOTH)

    mainframe.focus_force()

    return chosen_date.get()

def select_files():
    """Opens a window to select one or more files to import."""

    root = Tk()
    root.withdraw()

    paths = askopenfilenames()

    root.destroy()
    return paths

def add_treeview(df, treeview):
    """Adds imported items to main_gui treeview"""

    df['SELL BY'] = df['SELL BY'].dt.date

 # clear previous contents
    for i in treeview.get_children():
        treeview.delete(i)

    treeview.column("#0", width=0, stretch=False)

    # add column names
    columns = ["DELIVERY", "ITEM", "DESCRIPTION", "SELL BY", "QUANTITY"]
    treeview["columns"] = columns

    for i in columns:
        treeview.column(i, anchor="w")
        treeview.heading(i, text=i, anchor='w')

    # add data
    for index, row in df.iterrows():
        values = [row[col] for col in columns]
        print(values)
        treeview.insert("", "end", values=values)