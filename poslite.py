import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import sqlite3


def eh_treeListSelected(event):
# Event handler for treeItemList select
    global rowIndex
    
    for selected_item in treeItemList.selection():
        rowIndex = treeItemList.index(selected_item)
        print('index@select=' + str(rowIndex))
    

def eh_varBarcode(varBarcode):
# event handler for varBarcode
# if 10 characters of barcode entered, this function will automatically fetch the item name and unit price from database
# new row will be inserted into treeItemList
# Bill total will be recalculated

    global cur
    
    if len(varBarcode.get()) > 9:
        cur.execute("SELECT item_name, unit_price from items where item_code = '" + varBarcode.get() + "'")
        row = cur.fetchone()
        if row is None:
            print('Item not found')
        else:
            varItemName.set(row[0])
            varUnitPrice = float(row[1])
            varQuantity = 1.0
            varItemPrice = varUnitPrice * varQuantity
            strQuantity = str(varQuantity)
            strUnitPrice = str(varUnitPrice)
            strItemPrice = str(varItemPrice)
            treeItemList.insert("", tk.END, values=(varBarcode.get(), varItemName.get(), strQuantity, strUnitPrice, strItemPrice))
            varBarcode.set('')
            getItemTotal()
        
        
def eh_keyClick(event, arg):
# event handler for key click to capture arrow, tab and del keys
# if tab clicked, the focus will be set to the first row in the treeItemList
# if del clicked within treeItemList, current row will be deleted and focus will be set to next available row
# if right arrow clicked, item quantity will be incremented by 1 and price will be recalculated
# if left arrow clicked, item quantity will be decremented by 1 and price will be recalculated
# Bill total will be recalculated

    global rowIndex
    global varBillTotal
    
    print(arg, root.focus_get())
    curItem = treeItemList.focus()
    nextItem = treeItemList.next(curItem)
    prevItem = treeItemList.prev(curItem)    
    #print('tree values:', treeItemList.item(curItem)["values"])
        
    if (arg == 'Tab'):
        if (str(root.focus_get()) == '.!panedwindow.!frame.!entry'):
                if (len(treeItemList.get_children()) > 0):
                    curItem = treeItemList.get_children()[0]
                    treeItemList.focus(curItem)
                    treeItemList.selection_set(curItem)   
                    getItemTotal()

    if (arg == 'Delete'):
        if (str(root.focus_get()) == '.!panedwindow.!frame2.!treeview'):
            if (len(treeItemList.get_children()) > 0):
                treeItemList.delete(curItem)
                if (len(treeItemList.get_children()) > 0):
                    if (nextItem != ''):
                        curItem = nextItem
                    elif (prevItem != ''):
                        curItem = prevItem
                    else:
                        curItem = ''
                    treeItemList.focus(curItem)
                    treeItemList.selection_set(curItem)
                    getItemTotal()

    if (arg == 'Right'):
        if (str(root.focus_get()) == '.!panedwindow.!frame2.!treeview'):
            if (len(treeItemList.get_children()) > 0):
                tempValues = treeItemList.item(curItem)["values"]
                print(str(tempValues[1]))
                treeItemList.delete(curItem)
                varQuantity = float(tempValues[2])
                varQuantity = varQuantity + 1
                varUnitPrice = float(tempValues[3])
                varItemPrice = varUnitPrice * varQuantity
                tempValues[2] = str(varQuantity)
                tempValues[4] = str(varItemPrice)
                treeItemList.insert("", rowIndex, values=(tempValues))
                curItem = treeItemList.get_children()[rowIndex]
                print(treeItemList.get_children()[rowIndex])
                treeItemList.focus(curItem)
                treeItemList.selection_set(curItem)
                getItemTotal()
                  
    if (arg == 'Left'):
        if (str(root.focus_get()) == '.!panedwindow.!frame2.!treeview'):
            if (len(treeItemList.get_children()) > 0):
                tempValues = treeItemList.item(curItem)["values"]
                print(str(tempValues[1]))
                treeItemList.delete(curItem)
                varQuantity = float(tempValues[2])
                if (varQuantity > 1):
                    varQuantity = varQuantity - 1
                varUnitPrice = float(tempValues[3])
                varItemPrice = varUnitPrice * varQuantity
                tempValues[2] = str(varQuantity)
                tempValues[4] = str(varItemPrice)
                treeItemList.insert("", rowIndex, values=(tempValues))
                curItem = treeItemList.get_children()[rowIndex]
                print(treeItemList.get_children()[rowIndex])
                treeItemList.focus(curItem)
                treeItemList.selection_set(curItem)
                getItemTotal()

                
def getItemTotal():
# Common function to recalculate and display the Bill total.
# Called by all treeItemList event handlers

    varItemTotal = 0
    itemList = treeItemList.get_children()
    for itemLine in itemList:
        varItemTotal += float(treeItemList.item(itemLine)['values'][4])
    print('tot:', varItemTotal) 
    varBillTotal.set(str(varItemTotal))

    
########################################
# Main Section
########################################

# Create main window with a theme and title
root = ThemedTk(theme="radiance")
root.title("Point Of Sale")

# Declare Global variables
rowIndex = 0
varBarcode = tk.StringVar()
varItemName = tk.StringVar()
varUnitPrice = tk.DoubleVar()
varQuantity = tk.DoubleVar()
varItemPrice = tk.DoubleVar()
varBillTotal = tk.StringVar()

# Screen Title
labelForm = ttk.Label(root, text="BILLING")
labelForm.pack(padx=0,pady=10)

# Create Panedwindow  
panedwindow=ttk.Panedwindow(root)  
panedwindow.pack()  

# Create Frames  
frameEntry=ttk.Frame(panedwindow,width=600,height=50)  
frameList=ttk.Frame(panedwindow,width=600,height=300)  
frameSummary=ttk.Frame(panedwindow,width=600,height=50)  

# Assign Frames to Panedwindow
panedwindow.add(frameEntry, weight=1)  
panedwindow.add(frameList, weight=4)
panedwindow.add(frameSummary, weight=4)

# Create entryBarcode label and text box and place it within frameEntry to capture barcode
# Bind variable varBarcode to entryBarcode
# Bind event handler eh_varBarcode to varBarcode
labelBarcode = ttk.Label(frameEntry, text=u"Barcode:")
labelBarcode.grid(column=1, row=1, sticky=tk.W)
varBarcode.trace("w", lambda name, index, mode, varBarcode=varBarcode: eh_varBarcode(varBarcode))
entryBarcode = ttk.Entry(frameEntry, textvariable=varBarcode, font="Helvetica 11", width=14)
entryBarcode.grid(column=2, row=1, sticky=tk.W)
entryBarcode.focus()

# Create treeItemList and place it within frameList
columns = ('#1', '#2', '#3', '#4', '#5')
treeItemList = ttk.Treeview(frameList, columns=columns, show='headings', selectmode='browse')
treeItemList.grid(row=0, column=0, sticky='nsew')
treeItemList.heading('#1', text='Item Code')
treeItemList.heading('#2', text='Item Name')
treeItemList.heading('#3', text='Quantity')
treeItemList.heading('#4', text='Unit Price')
treeItemList.heading('#5', text='Cost')
treeItemList.column("#1",minwidth=0,width=100)
treeItemList.column("#2",minwidth=0,width=500)
treeItemList.column("#3",minwidth=0,width=60,anchor='e')
treeItemList.column("#4",minwidth=0,width=150,anchor='e')
treeItemList.column("#5",minwidth=0,width=150,anchor='e')

# Create scrollbar and assign to treeItemList
scrollbar = ttk.Scrollbar(frameList, orient=tk.VERTICAL, command=treeItemList.yview)
treeItemList.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

# Create entryBillTotal label and text box and place it within frameSummary to display bill total
labelBillTotal = ttk.Label(frameSummary, text=u"Bill Total:")
labelBillTotal.grid(column=1, row=1, sticky=tk.W)
entryBillTotal = ttk.Entry(frameSummary, textvariable=varBillTotal, font="Helvetica 11", width=14, justify="right")
entryBillTotal.grid(column=2, row=1, sticky=tk.E)
entryBillTotal.config(state='disabled')

# Declare Event Handlers
treeItemList.bind('<<TreeviewSelect>>', eh_treeListSelected)
root.bind('<Left>',lambda event,arg='Left':eh_keyClick(event,arg))
root.bind('<Right>',lambda event,arg='Right':eh_keyClick(event,arg))
root.bind('<Up>',lambda event,arg='Up':eh_keyClick(event,arg))
root.bind('<Down>',lambda event,arg='Down':eh_keyClick(event,arg))
root.bind('<Tab>',lambda event,arg='Tab':eh_keyClick(event,arg))
root.bind('<Delete>',lambda event,arg='Delete':eh_keyClick(event,arg))

# Create Database connection
conn = sqlite3.connect("POSLITE")
cur = conn.cursor()

# Call Main Loop  
root.mainloop()
