import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import *
from db_query import *
from datetime import datetime

def inv_date_win():

    # Set up main window
    query_root = tk.Toplevel()

    mainframe = Frame(query_root)
    mainframe.pack(fill=BOTH, expand=TRUE)

    # Create input fields & labels in mainframe
    input_frame = ttk.Frame(mainframe)
    input_frame.pack(side=TOP, fill=BOTH, expand=FALSE)
    
    item_label = Label(input_frame, text="Item")
    item_label.grid(column=0, row=0, sticky="W")
    
    item = StringVar()
    item_entry = Entry(input_frame, width=7, textvariable=item)
    item_entry.grid(column=1, row=0, sticky="W")

    after_date_lbl = Label(input_frame, text="After date:")
    after_date_lbl.grid(column=0, row=1, sticky="W")
    
    after_date = StringVar()
    after_date_ent = DateEntry(input_frame, width=15, textvariable=after_date)
    after_date_ent.grid(column=1, row=1, sticky="NESW")

    before_date_lbl = Label(input_frame, text="Before date:")
    before_date_lbl.grid(column=0, row=2, sticky="W")
    
    before_date = StringVar()
    before_date_ent = DateEntry(input_frame, width=15, textvariable=before_date)
    before_date_ent.grid(column=1, row=2, sticky="W")

    # Create display for results of the query in mainframe
    display_frame = ttk.Frame(mainframe, height=250, padding= 10, width=500)
    display_frame.pack(side=BOTTOM, fill=BOTH, expand=TRUE)

    treeview = ttk.Treeview(display_frame)
    treeview.pack(fill=BOTH, expand=TRUE)

    ok_button = Button(display_frame, text="OK", command=
                       lambda: get_df(item.get(), after_date.get(), before_date.get(), treeview))
    ok_button.pack(side=LEFT, fill=X, expand=TRUE)

    cancel_button = Button(display_frame, text="Cancel", command= query_root.destroy)
    cancel_button.pack(side=RIGHT, fill=X, expand=TRUE)

    # Add padding around all elements
    for child in input_frame.winfo_children(): 
        child.grid_configure(padx=5, pady=5)


def add_df_to_treeview(df, treeview):
    """Adds query to treeview"""
    
    # clear previous contents
    for i in treeview.get_children():
        treeview.delete(i)

    # add column names
    columns = ["DELIVERY", "ITEM", "DESCRIPTION", "SELL BY", "QUANTITY"]
    treeview["columns"] = columns

    for i in columns:
        treeview.column(i, anchor="w")
        treeview.heading(i, text=i, anchor='w')

    # add data
    for index, row in df.iterrows():
        values = [row[col] for col in columns]
        treeview.insert("", "end", values=values)

def get_df(item, after_date, before_date, treeview):

    df = db_query_date(item, after_date, before_date)

    print(df)

    add_df_to_treeview(df, treeview)