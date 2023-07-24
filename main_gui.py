import tkinter as tk
from tkinter import *
from tkinter import ttk
from query_gui import *
from aid_import import *
from aid_import_def import *
from db_query import *

def provision_name():
    stuff

def main_gui():

    root = tk.Tk()
    root_title = "placeholder"
    main = tk_init(root, root_title)

    imp_tree = ttk.Treeview(main.mainframe)
    imp_tree.pack(fill=BOTH, expand=TRUE, side=TOP)

    import_button = Button(main.mainframe, text="Import", command=aid_import)
    import_button.pack(fill=X, expand=TRUE, side=LEFT)

    db_query_date = Button(main.mainframe, text="Short Date Query", command=inv_date_win)
    db_query_date.pack(fill=X, expand=TRUE, side=RIGHT)

    for child in main.root.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

