import tkinter as tk
from tkinter import *
from tkinter import ttk
from query_gui import *
from aid_import import *
from aid_import_def import *
from db_query import *
import yaml

#initialize tk frames
class tk_init:
    def __init__(self, root, title):
        self.root = root
        self.root.title(title)
        self.mainframe = ttk.Frame(self.root)
        self.mainframe.pack(fill=BOTH, expand=TRUE)

def provision_name():
    """Gather company name from config."""
    with open('config.yaml', 'r') as file:
        config=yaml.safe_load(file)
    
    name = f"AID - {config['company']}"
    return name

def version_name():
    """Gather program version from config."""
    with open('config.yaml', 'r') as file:
        config=yaml.safe_load(file)
    
    name = config['software_version']
    return name

def main_gui():
    """Set up main GUI."""

    root = tk.Tk()
    root_title = provision_name()
    main = tk_init(root, root_title)

    imp_tree = ttk.Treeview(main.mainframe)
    imp_tree.pack(side=TOP, fill=BOTH, expand=TRUE)

    import_button = Button(main.mainframe, text="Import", command=lambda: aid_import(imp_tree, root))
    import_button.pack(side=LEFT, fill=X, expand=TRUE)

    db_query_date = Button(main.mainframe, text="Short Date Query", command=inv_date_win)
    db_query_date.pack(side=RIGHT, fill=X, expand=TRUE)

    for child in main.root.winfo_children(): 
        child.grid_configure(padx=5, pady=5)


    root.mainloop()

