import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import sqlite3


def event_treeListSelected(event):
# Event handler for tk_tree_bill_items select
    global tree_idx
    
    for tree_row_selected in tk_tree_bill_items.selection():
        tree_idx = tk_tree_bill_items.index(tree_row_selected)
        print('index@select=' + str(tree_idx))
    

def event_bind_barcode(bind_barcode):
# event handler for bind_barcode
# if 10 characters of barcode entered, this function will automatically fetch the item name and unit price from database
# new row will be inserted into tk_tree_bill_items
# Bill total will be recalculated

    global db_cur
    global tree_row_prev
    
    if len(bind_barcode.get()) > 9:
        db_cur.execute("SELECT item_name, unit_price from items where item_code = '" + bind_barcode.get() + "'")
        db_item_row = db_cur.fetchone()
        if db_item_row is None:
            print('Item not found')
        else:
            item_name.set(db_item_row[0])
            unit_price = float(db_item_row[1])
            item_qty = 1.0
            item_price = unit_price * item_qty
            if (tree_row_prev == 'evenrow'):
                tree_row_curr = 'oddrow'
            else:
                tree_row_curr = 'evenrow'            
            tk_tree_bill_items.insert("", tk.END, values=(bind_barcode.get(), item_name.get(), str(item_qty), str(unit_price), str(item_price)), tags=(tree_row_curr,))
            bind_barcode.set('')
            get_item_total()
            tree_row_prev = tree_row_curr
        
def event_keyClick(event, arg):
# event handler for key click to capture arrow, tab and del keys
# if tab clicked, the focus will be set to the first row in the tk_tree_bill_items
# if del clicked within tk_tree_bill_items, current row will be deleted and focus will be set to next available row
# if right arrow clicked, item quantity will be incremented by 1 and price will be recalculated
# if left arrow clicked, item quantity will be decremented by 1 and price will be recalculated
# Bill total will be recalculated

    global tree_idx
    global bind_bill_tot
    
    print(arg, tk_root.focus_get())
    tree_row_curr = tk_tree_bill_items.focus()
    tree_row_next = tk_tree_bill_items.next(tree_row_curr)
    tree_row_prev = tk_tree_bill_items.prev(tree_row_curr)    
    #print('tree values:', tk_tree_bill_items.item(tree_row_curr)["values"])
        
    if (arg == 'Tab'):
        if (str(tk_root.focus_get()) == '.!panedwindow.!frame.!entry'):
                if (len(tk_tree_bill_items.get_children()) > 0):
                    tree_row_curr = tk_tree_bill_items.get_children()[0]
                    tk_tree_bill_items.focus(tree_row_curr)
                    tk_tree_bill_items.selection_set(tree_row_curr)   
                    get_item_total()

    if (arg == 'Delete'):
        if (str(tk_root.focus_get()) == '.!panedwindow.!frame2.!treeview'):
            if (len(tk_tree_bill_items.get_children()) > 0):
                tk_tree_bill_items.delete(tree_row_curr)
                if (len(tk_tree_bill_items.get_children()) > 0):
                    if (tree_row_next != ''):
                        tree_row_curr = tree_row_next
                    elif (tree_row_prev != ''):
                        tree_row_curr = tree_row_prev
                    else:
                        tree_row_curr = ''
                    tk_tree_bill_items.focus(tree_row_curr)
                    tk_tree_bill_items.selection_set(tree_row_curr)
            get_item_total()

    if (arg == 'Right'):
        if (str(tk_root.focus_get()) == '.!panedwindow.!frame2.!treeview'):
            if (len(tk_tree_bill_items.get_children()) > 0):
                tree_row_values = tk_tree_bill_items.item(tree_row_curr)["values"]
                tree_row_tags = tk_tree_bill_items.item(tree_row_curr)["tags"]
                print(str(tree_row_values[1]))
                tk_tree_bill_items.delete(tree_row_curr)
                item_qty = float(tree_row_values[2])
                item_qty = item_qty + 1
                unit_price = float(tree_row_values[3])
                item_price = unit_price * item_qty
                tree_row_values[2] = str(item_qty)
                tree_row_values[4] = str(item_price)
                tk_tree_bill_items.insert("", tree_idx, values=(tree_row_values), tags=(tree_row_tags))
                tree_row_curr = tk_tree_bill_items.get_children()[tree_idx]
                print(tk_tree_bill_items.get_children()[tree_idx])
                tk_tree_bill_items.focus(tree_row_curr)
                tk_tree_bill_items.selection_set(tree_row_curr)
            get_item_total()
                  
    if (arg == 'Left'):
        if (str(tk_root.focus_get()) == '.!panedwindow.!frame2.!treeview'):
            if (len(tk_tree_bill_items.get_children()) > 0):
                tree_row_values = tk_tree_bill_items.item(tree_row_curr)["values"]
                tree_row_tags = tk_tree_bill_items.item(tree_row_curr)["tags"]                
                print(str(tree_row_values[1]))
                tk_tree_bill_items.delete(tree_row_curr)
                item_qty = float(tree_row_values[2])
                if (item_qty > 1):
                    item_qty = item_qty - 1
                unit_price = float(tree_row_values[3])
                item_price = unit_price * item_qty
                tree_row_values[2] = str(item_qty)
                tree_row_values[4] = str(item_price)
                tk_tree_bill_items.insert("", tree_idx, values=(tree_row_values), tags=(tree_row_tags))
                tree_row_curr = tk_tree_bill_items.get_children()[tree_idx]
                print(tk_tree_bill_items.get_children()[tree_idx])
                tk_tree_bill_items.focus(tree_row_curr)
                tk_tree_bill_items.selection_set(tree_row_curr)
            get_item_total()

                
def get_item_total():
# Common function to recalculate and display the Bill total.
# Called by all tk_tree_bill_items event handlers

    item_total = 0
    tree_rows = tk_tree_bill_items.get_children()
    for tree_row in tree_rows:
        item_total += float(tk_tree_bill_items.item(tree_row)['values'][4])
    print('tot:', item_total) 
    bind_bill_tot.set(str(item_total))

    
########################################
# Main Section
########################################

# Create main window with a theme and title
tk_root = ThemedTk(theme="radiance")
tk_root.title("Point Of Sale")

# Declare Global variables
tree_idx = 0
tree_row_prev = 'evenrow'

# Declare Bind variables
bind_barcode = tk.StringVar()
bind_bill_tot = tk.StringVar()

# Declare working variables
item_name = tk.StringVar()
unit_price = tk.DoubleVar()
item_qty = tk.DoubleVar()
item_price = tk.DoubleVar()

# Screen Title
tk_label_form = ttk.Label(tk_root, text="BILLING")
tk_label_form.pack(padx=0,pady=10)

# Create Panedwindow  
tk_panwin=ttk.Panedwindow(tk_root)  
tk_panwin.pack()  

# Create Frames  
tk_frame_entry=ttk.Frame(tk_panwin,width=600,height=50)  
tk_frame_list=ttk.Frame(tk_panwin,width=600,height=300)  
tk_frame_summary=ttk.Frame(tk_panwin,width=600,height=50)  

# Assign Frames to Panedwindow
tk_panwin.add(tk_frame_entry, weight=1)  
tk_panwin.add(tk_frame_list, weight=4)
tk_panwin.add(tk_frame_summary, weight=4)

# Create tk_entry_barcode label and text box and place it within frame_entry to capture barcode
# Bind variable varBarcode to tk_entry_barcode
# Bind event handler eh_varBarcode to varBarcode
tk_label_barcode = ttk.Label(tk_frame_entry, text=u"Barcode:")
tk_label_barcode.grid(column=1, row=1, sticky=tk.W)
bind_barcode.trace("w", lambda name, index, mode, bind_barcode=bind_barcode: event_bind_barcode(bind_barcode))
tk_entry_barcode = ttk.Entry(tk_frame_entry, textvariable=bind_barcode, font="Helvetica 11", width=14)
tk_entry_barcode.grid(column=2, row=1, sticky=tk.W)
tk_entry_barcode.focus()

# Create tk_tree_bill_items and place it within tk_frame_list
tree_columns = ('#1', '#2', '#3', '#4', '#5')
tk_tree_bill_items = ttk.Treeview(tk_frame_list, columns=tree_columns, show='headings', selectmode='browse')
tk_tree_bill_items.grid(row=0, column=0, sticky='nsew')
tk_tree_bill_items.heading('#1', text='Item Code')
tk_tree_bill_items.heading('#2', text='Item Name')
tk_tree_bill_items.heading('#3', text='Quantity')
tk_tree_bill_items.heading('#4', text='Unit Price')
tk_tree_bill_items.heading('#5', text='Cost')
tk_tree_bill_items.column("#1",minwidth=0,width=100)
tk_tree_bill_items.column("#2",minwidth=0,width=500)
tk_tree_bill_items.column("#3",minwidth=0,width=60,anchor='e')
tk_tree_bill_items.column("#4",minwidth=0,width=150,anchor='e')
tk_tree_bill_items.column("#5",minwidth=0,width=150,anchor='e')

# Create tk_scbar_bill_items and assign to tk_tree_bill_items
tk_scbar_bill_items = ttk.Scrollbar(tk_frame_list, orient=tk.VERTICAL, command=tk_tree_bill_items.yview)
tk_tree_bill_items.configure(yscroll=tk_scbar_bill_items.set)
tk_tree_bill_items.tag_configure('oddrow', background='bisque')
tk_scbar_bill_items.grid(row=0, column=1, sticky='ns')

# Create entryBillTotal label and text box and place it within tk_frame_summary to display bill total
tk_label_bill_tot = ttk.Label(tk_frame_summary, text=u"Bill Total:")
tk_label_bill_tot.grid(column=1, row=1, sticky=tk.W)
tk_entry_bill_tot = ttk.Entry(tk_frame_summary, textvariable=bind_bill_tot, font="Helvetica 11", width=14, justify="right")
tk_entry_bill_tot.grid(column=2, row=1, sticky=tk.E)
tk_entry_bill_tot.config(state='disabled')

# Declare Event Handlers
tk_tree_bill_items.bind('<<TreeviewSelect>>', event_treeListSelected)
tk_root.bind('<Left>',lambda event,arg='Left':event_keyClick(event,arg))
tk_root.bind('<Right>',lambda event,arg='Right':event_keyClick(event,arg))
tk_root.bind('<Up>',lambda event,arg='Up':event_keyClick(event,arg))
tk_root.bind('<Down>',lambda event,arg='Down':event_keyClick(event,arg))
tk_root.bind('<Tab>',lambda event,arg='Tab':event_keyClick(event,arg))
tk_root.bind('<Delete>',lambda event,arg='Delete':event_keyClick(event,arg))

# Create Database connection
db_conn = sqlite3.connect("POSLITE")
db_cur = db_conn.cursor()

# Call Main Loop  
tk_root.mainloop()
