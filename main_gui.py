import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from query_gui import *
from aid_import import *
from aid_import_def import *
from db_query import *
import yaml

#initialize tk frames
class Tk_init:
    def __init__(self, root, title, geo):
        self.root = root
        self.root.title(title)
        self.root.geometry(geo)
        self.mainframe = ttk.Frame(self.root)
        self.mainframe.grid(sticky='nsew')

def provision_name(new_dir):
    """Create a config file if not exists, then gather company name from config."""
    
    config_path = os.path.join(new_dir, "config.yaml")
    if os.path.exists(config_path) == False:
        name_input = tk.simpledialog.askstring('User Setup', 'What is the name of the company?')
        with open(config_path, "a") as f:
            config=yaml.safe_dump({'company': name_input, 'software_version': '1.0' }, f)

    with open(config_path, 'r') as file:
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
    """Create home directory, connect, and create main GUI."""

    home_dir = os.path.expanduser("~")

    # Create a new directory in the user's home directory
    new_dir = os.path.join(home_dir, "AID")
    os.makedirs(new_dir, exist_ok=True)

    # Connect to the database file in the new directory
    db_path = os.path.join(new_dir, "invoice_db.db")
    conn = sqlite3.connect(db_path)  

    # Create new main gui window
    root = tk.Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root_title = provision_name(new_dir)
    geo = "1500x700"
    
    main = Tk_init(root, root_title, geo)

    imp_tree = ttk.Treeview(main.mainframe)
    imp_tree.grid(sticky='nsew')

    main.mainframe.grid_columnconfigure(0, weight=1)
    main.mainframe.grid_rowconfigure(0, weight=1)

    import_button = Button(main.mainframe, text="Import", command=lambda: aid_import(imp_tree, root, conn))
    import_button.grid(sticky='ew')

    db_query_date = Button(main.mainframe, text="Short Date Query", command=lambda: inv_date_win(conn))
    db_query_date.grid(sticky='ew')

    for child in main.mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    def on_closing():
        conn.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

