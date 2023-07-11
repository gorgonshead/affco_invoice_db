import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import *

#initialize tk frames
def tk_window():
    
    def open_calendar(event):
        selected_date = StringVar()
        after_date.set(selected_date.get())
        after_date_ent.config(textvariable=selected_date.get)

    root = Tk()
    root.title("Short Date Search")
    
    mainframe = ttk.Frame(root)
    mainframe.pack()


    display_frame = ttk.Frame(root, height=250, padding= 10, width=500)
    display_frame.pack(fill=BOTH, side=BOTTOM, expand=TRUE)

    display_lbx = Listbox(display_frame)
    display_lbx.pack(fill=BOTH, expand=TRUE)

    item_label = Label(mainframe, text="Item")
    item_label.grid(column=0, row=0, sticky="W")
    
    item = StringVar()
    item_entry = Entry(mainframe, width=7, textvariable=item)
    item_entry.grid(column=1, row=0, sticky="W")

    after_date_lbl = Label(mainframe, text="After date:")
    after_date_lbl.grid(column=0, row=1, sticky="W")
    
    after_date = StringVar()
    after_date_ent = DateEntry(mainframe, width=15, textvariable=after_date)
    after_date_ent.grid(column=1, row=1, sticky="NESW")

    before_date_lbl = Label(mainframe, text="Before date:")
    before_date_lbl.grid(column=0, row=2, sticky="W")
    
    before_date = StringVar()
    before_date_ent = DateEntry(mainframe, width=15, textvariable=before_date)
    before_date_ent.grid(column=1, row=2, sticky="W")

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

    root.mainloop()