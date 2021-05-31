import PySimpleGUI as sg
import mariadb
import datetime
import json
import sys
import platform
from pynput.keyboard import Key, Controller


######
# Process Barcode field input
def proc_barcode(barcode):
    if len(barcode) > 12:
        db_pos_sql_stmt = "SELECT item_code, item_name, uom, selling_price, cgst_tax_rate, sgst_tax_rate from tabItem where barcode = %s"
        db_pos_sql_data = (barcode,)
        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")       
            db_pos_conn.close()
            sys.exit(1)
            
        db_item_row = db_pos_cur.fetchone()
        if db_item_row is None:
            print('Item not found')
        else:
            item_code = db_item_row[0]
            item_name = db_item_row[1]
            uom = db_item_row[2]
            qty = 1
            selling_price = db_item_row[3]
            cgst_tax_rate = db_item_row[4]
            sgst_tax_rate = db_item_row[5]
            row_item = []
            row_item.append(item_code)
            row_item.append(barcode)
            row_item.append(item_name)
            row_item.append(uom)
            row_item.append(qty)            
            row_item.append("{:.2f}".format(selling_price))
            selling_amount = float(qty) * float(selling_price)
            row_item.append("{:.2f}".format(selling_amount))                                    
            tax_rate = float(cgst_tax_rate) + float(sgst_tax_rate)
            row_item.append(tax_rate)                        
            tax_amount = selling_amount * tax_rate / 100
            row_item.append("{:.2f}".format(tax_amount))
            net_price = selling_amount + tax_amount
            row_item.append("{:.2f}".format(net_price))
            row_item.append(cgst_tax_rate)                        
            row_item.append(sgst_tax_rate)      
            list_items.append(row_item)
            window.Element('-TABLE-').update(values=list_items)
            window.Element('-BARCODE-NB-').update(value='')
            window.Element('-BARCODE-NB-').set_focus()
            sum_item_list()


######
# Compute Invoice Summary fields
def sum_item_list():
    line_items = 0
    total_qty = 0.0
    total_price = 0.0
    total_tax = 0.0
    total_cgst = 0.0
    total_sgst = 0.0
    total_net_price = 0.0
    
    for row_item in list_items:
        line_items += 1
        total_qty += float(row_item[4])
        total_price += float(row_item[6])
        total_tax += float(row_item[8])
        total_net_price += float(row_item[9])
        total_cgst += float(row_item[10])
        total_sgst += float(row_item[11])
    
    window.Element('-LINE-ITEMS-').update(value=str(line_items))
    window.Element('-TOTAL-QTY-').update(value="{:.2f}".format(total_qty))
    window.Element('-TOTAL-PRICE-').update(value="{:.2f}".format(total_price))
    window.Element('-TOTAL-TAX-').update(value="{:.2f}".format(total_tax))
    window.Element('-NET-PRICE-').update(value="{:.2f}".format(total_net_price))
    window.Element('-INVOICE-AMT-').update(value="{:.2f}".format(total_net_price))
    window.Element('-TOTAL-CGST-').update(value="{:.2f}".format(total_cgst))
    window.Element('-TOTAL-SGST-').update(value="{:.2f}".format(total_sgst))


######
# Popup window for Change Quantity
def open_popup_chg_qty(row_item, list_item):
    layout_chg_qty = [
        [sg.Text(str(list_item[2]), size=(30,2),  font=("Helvetica Bold", 12))],
        [sg.Text('Existing Quantity:', size=(15,1),  font=("Helvetica", 11)),     
         sg.Input(key='-EXISTING-QTY-',readonly=True, background_color='gray89', disabled_readonly_text_color=disabled_text_color,font=("Helvetica", 11),size=(15,1))],
        [sg.Text('New Quantity:', size=(15,1),  font=("Helvetica", 11)),             
         sg.Input(key='-NEW-QTY-',readonly=False, focus=True, background_color='white',font=("Helvetica", 11),size=(15,1), enable_events=True)],
        [sg.Text('')],
        [sg.Button('F12-Ok', size=(8, 1), font='Calibri 12 bold', key='-CHG-QTY-OK-', button_color = pad_button_color),
         sg.Button('Esc-Exit', size=(8, 1), font='Calibri 12 bold', key='-CHG-QTY-ESC-', button_color = pad_button_color)]           
    ]   

    popup_chg_qty = sg.Window("Change Quantity", layout_chg_qty, location=(300,250), size=(350,180), modal=True, finalize=True,return_keyboard_events=True)
    popup_chg_qty.Element('-EXISTING-QTY-').update(value=str(list_item[4]))
    
    while True:
        event, values = popup_chg_qty.read()
        print('eventc=', event)
        
        if event in ("Exit", '-CHG-QTY-ESC-', 'Escape:27') or event == sg.WIN_CLOSED:
            break        
        if event == "-CHG-QTY-OK-" or event == "F12:123": 
            applied_qty = popup_chg_qty.Element('-NEW-QTY-').get()
            if (applied_qty.isnumeric() or applied_qty.replace('.', '', 1).isdigit()):
                tax_rate = list_items[row_item][7]
                selling_price = list_items[row_item][6]
                selling_amount = float(applied_qty) * float(selling_price)
                tax_amount = selling_amount * float(tax_rate) / 100
                net_price = selling_amount + tax_amount            
                list_items[row_item][4] = applied_qty
                list_items[row_item][6] = "{:.2f}".format(selling_amount)
                list_items[row_item][8] = "{:.2f}".format(tax_amount)
                list_items[row_item][9] = "{:.2f}".format(net_price)
                window.Element('-TABLE-').update(values=list_items, select_rows=[row_item])
                #sum_item_list()
                break   
    popup_chg_qty.close()   


######
# Save the Invoice to DB
def save_invoice():
    reference_number = window.Element('-REFERENCE_NO-').get()
    if reference_number == '':
        insert_invoice()
    else:
        update_invoice()
    
        
def insert_invoice():
    print('insert')
    if len(list_items) == 0:
        return
    db_pos_sql_stmt = "SELECT nextval('REFERENCE_NUMBER')"
    try:
        db_pos_cur.execute(db_pos_sql_stmt)
    except mariadb.Error as db_err:
        print(f"POS database error: {db_err}")       
        db_pos_conn.close()
        sys.exit(1)
    print('ref no')
            
    db_item_row = db_pos_cur.fetchone()
    if db_item_row is None:
        print('Sequence not found')
    else:
        reference_number = db_item_row[0]
    print(reference_number)
    total_amount = window.Element('-TOTAL-PRICE-').get()
    net_amount = window.Element('-NET-PRICE-').get()
    invoice_amount = window.Element('-INVOICE-AMT-').get()
    cgst_tax_amount = window.Element('-TOTAL-CGST-').get()
    sgst_tax_amount = window.Element('-TOTAL-SGST-').get()
    terminal_id = window.Element('-TERMINAL-').get()  
    
    db_pos_sql_stmt = ("INSERT INTO tabInvoice (name, posting_date, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, terminal_id, creation, owner)"
                        "VALUES (%s, now(), %s, %s, %s, %s, %s, %s, now(), %s)")
    db_pos_sql_data = (reference_number, '0000000000', total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, terminal_id, ws_erp_user)
    try:
        db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
    except mariadb.Error as db_err:
        print(f"POS database error: {db_err}")    
        db_pos_conn.rollback()
        db_pos_conn.close()
        sys.exit(1)
    
    item_count = 0
    for row_item in list_items:
        item_count += 1
        item_code = row_item[0]
        qty = row_item[4]
        selling_price = row_item[6]
        total_cgst = row_item[10]
        total_sgst = row_item[11]
        name = reference_number + f"{item_count:04d}"
        print(name)

        db_pos_sql_stmt = ("INSERT INTO `tabInvoice Item` (name, parent, item_code, qty, standard_selling_price, applied_selling_price, cgst_tax_amount, sgst_tax_amount)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        db_pos_sql_data = (name, reference_number, item_code, qty, selling_price, selling_price, cgst_tax_amount, sgst_tax_amount)
        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")    
            db_pos_conn.rollback()
            db_pos_conn.close()
            sys.exit(1)    
    db_pos_conn.commit()


def update_invoice():
    print('update')
    reference_number = window.Element('-REFERENCE_NO-').get()
    mobile_number = window.Element('-MOBILE_NO-').get()
    total_amount = window.Element('-TOTAL-PRICE-').get()
    invoice_amount = window.Element('-INVOICE-AMT-').get()
    cgst_tax_amount = window.Element('-TOTAL-CGST-').get()
    sgst_tax_amount = window.Element('-TOTAL-SGST-').get()
    terminal_id = window.Element('-TERMINAL-').get()  
    reference_number = window.Element('-REFERENCE_NO-').get()  
    
    db_pos_sql_stmt = ("UPDATE tabInvoice SET posting_date=now(), customer=%s, total_amount=%s, cgst_tax_amount=%s, sgst_tax_amount=%s, invoice_amount=%s, terminal_id=%s, creation=now(), owner=%s"
                        " WHERE name = %s")
    db_pos_sql_data = (mobile_number, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, terminal_id, ws_erp_user, reference_number)
    try:
        db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
    except mariadb.Error as db_err:
        print(f"POS database error: {db_err}")    
        db_pos_conn.rollback()
        db_pos_conn.close()
        sys.exit(1)
    print('here1', reference_number)
    db_pos_sql_stmt = ("DELETE FROM `tabInvoice Item` WHERE parent = '" + reference_number + "'")
    
    try:
        db_pos_cur.execute(db_pos_sql_stmt)
    except mariadb.Error as db_err:
        print(f"POS database error: {db_err}")    
        db_pos_conn.rollback()
        db_pos_conn.close()
        sys.exit(1)
    print('here2')
 
    item_count = 0
    for row_item in list_items:
        item_count += 1
        item_code = row_item[0]
        qty = row_item[4]
        selling_price = row_item[6]
        total_cgst = row_item[10]
        total_sgst = row_item[11]
        name = reference_number + f"{item_count:04d}"
        print(name)

        db_pos_sql_stmt = ("INSERT INTO `tabInvoice Item` (name, parent, item_code, qty, standard_selling_price, applied_selling_price, cgst_tax_amount, sgst_tax_amount)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        db_pos_sql_data = (name, reference_number, item_code, qty, selling_price, selling_price, cgst_tax_amount, sgst_tax_amount)
        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")    
            db_pos_conn.rollback()
            db_pos_conn.close()
            sys.exit(1)
    db_pos_conn.commit()


def delete_invoice():
    print('delete')
    reference_number = window.Element('-REFERENCE_NO-').get()
    if reference_number == '':
        return
    db_pos_sql_stmt = ("DELETE FROM `tabInvoice Item` WHERE parent = '" + reference_number + "'")
    print(db_pos_sql_stmt)
    try:
        db_pos_cur.execute(db_pos_sql_stmt)
    except mariadb.Error as db_err:
        print(f"POS database error: {db_err}")    
        db_pos_conn.rollback()
        db_pos_conn.close()
        sys.exit(1)

    db_pos_sql_stmt = ("DELETE FROM `tabInvoice` WHERE name = '" + reference_number + "'")
    try:
        db_pos_cur.execute(db_pos_sql_stmt)
    except mariadb.Error as db_err:
        print(f"POS database error: {db_err}")    
        db_pos_conn.rollback()
        db_pos_conn.close()
        sys.exit(1)
    db_pos_conn.commit()


def clear_invoice():
    print('clear')
    
    line_items = 0
    total_qty  = 0
    total_price  = 0
    total_tax  = 0
    total_net_price  = 0
    total_cgst  = 0
    total_sgst  = 0
    list_items.clear()
    row_item = []
    window.Element('-LINE-ITEMS-').update(value=str(line_items))
    window.Element('-TOTAL-QTY-').update(value="{:.2f}".format(total_qty))
    window.Element('-TOTAL-PRICE-').update(value="{:.2f}".format(total_price))
    window.Element('-TOTAL-TAX-').update(value="{:.2f}".format(total_tax))
    window.Element('-NET-PRICE-').update(value="{:.2f}".format(total_net_price))
    window.Element('-INVOICE-AMT-').update(value="{:.2f}".format(total_net_price))
    window.Element('-TOTAL-CGST-').update(value="{:.2f}".format(total_cgst))
    window.Element('-TOTAL-SGST-').update(value="{:.2f}".format(total_sgst))
    window.Element('-TABLE-').update(values=list_items)     
    window.Element('-INVOICE_NO-').update(value='')
    window.Element('-REFERENCE_NO-').update(value='')
    window.Element('-MOBILE_NO-').update(value='')

    
def previous_invoice():
    print('prev')
    reference_number = window.Element('-REFERENCE_NO-').get()
    if (reference_number == ''):
        db_pos_sql_stmt = ("SELECT name, posting_date, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount from tabInvoice WHERE name = (select max(name) from tabInvoice)")
        try:
            db_pos_cur.execute(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")       
            db_pos_conn.close()
            sys.exit(1)
    else:
        db_pos_sql_stmt = ("SELECT name, posting_date, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount from tabInvoice WHERE name = (select max(name) from tabInvoice where name < %s)")
        db_pos_sql_data = (reference_number,)

        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")       
            db_pos_conn.close()
            sys.exit(1)
    
    db_invoice_row = db_pos_cur.fetchone()
    if db_invoice_row is None:
        print('Invoice not found')
    else:
        print('here1 ', db_invoice_row[0])
        reference_number = db_invoice_row[0]
        window.Element('-REFERENCE_NO-').update(value= reference_number)
        mobile_number = db_invoice_row[2]
        window.Element('-MOBILE_NO-').update(value= mobile_number)
        db_pos_sql_stmt = ("SELECT inv_item.item_code, item_name, barcode, uom, qty,standard_selling_price, applied_selling_price, cgst_tax_amount,sgst_tax_amount from `tabInvoice Item` inv_item, tabItem item WHERE inv_item.parent = %s and inv_item.item_code = item.item_code")
        db_pos_sql_data = (reference_number,)
        print(db_pos_sql_stmt)
        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")       
            db_pos_conn.close()
            sys.exit(1)
        print('here2 ', db_invoice_row[0])
            
        db_items = db_pos_cur.fetchall()
        row_item = []
        list_items.clear()
        
        for db_item_row in db_items:
            item_code = db_item_row[0]
            item_name = db_item_row[1]
            barcode = db_item_row[2]
            uom = db_item_row[3]
            qty = db_item_row[4]
            selling_price = db_item_row[5]
            cgst_tax_rate = db_item_row[7]
            sgst_tax_rate = db_item_row[8]
            selling_amount = float(qty) * float(selling_price)
            tax_rate = float(cgst_tax_rate) + float(sgst_tax_rate)
            tax_amount = selling_amount * tax_rate / 100
            net_amount = selling_amount + tax_amount  
            row_item.append(item_code)  
            row_item.append(barcode)  
            row_item.append(item_name)  
            row_item.append(uom)  
            row_item.append(qty)  
            row_item.append("{:.2f}".format(selling_price))  
            row_item.append("{:.2f}".format(selling_amount))  
            row_item.append("{:.2f}".format(tax_rate))  
            row_item.append("{:.2f}".format(tax_amount))  
            row_item.append("{:.2f}".format(selling_amount))  
            row_item.append("{:.2f}".format(net_amount))  
            row_item.append("{:.2f}".format(cgst_tax_rate))  
            row_item.append("{:.2f}".format(sgst_tax_rate))  
            list_items.append(row_item)
            window.Element('-TABLE-').update(values=list_items)
        sum_item_list()


def next_invoice():
    print('next')
    reference_number = window.Element('-REFERENCE_NO-').get()
    if (reference_number == ''):
        return
    else:
        db_pos_sql_stmt = ("SELECT name, posting_date, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount from tabInvoice WHERE name = (select min(name) from tabInvoice where name > %s)")
        db_pos_sql_data = (reference_number,)

        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")       
            db_pos_conn.close()
            sys.exit(1)
    
    db_invoice_row = db_pos_cur.fetchone()
    if db_invoice_row is None:
        print('Invoice not found')
    else:
        print('here1 ', db_invoice_row[0])
        reference_number = db_invoice_row[0]
        window.Element('-REFERENCE_NO-').update(value= reference_number)
        mobile_number = db_invoice_row[2]
        window.Element('-MOBILE_NO-').update(value= mobile_number)
        db_pos_sql_stmt = ("SELECT inv_item.item_code, item_name, barcode, uom, qty,standard_selling_price, applied_selling_price, cgst_tax_amount,sgst_tax_amount from `tabInvoice Item` inv_item, tabItem item WHERE inv_item.parent = %s and inv_item.item_code = item.item_code")
        db_pos_sql_data = (reference_number,)
        print(db_pos_sql_stmt)
        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")       
            db_pos_conn.close()
            sys.exit(1)
        print('here2 ', db_invoice_row[0])
            
        db_items = db_pos_cur.fetchall()
        row_item = []
        list_items.clear()
        
        for db_item_row in db_items:
            item_code = db_item_row[0]
            item_name = db_item_row[1]
            barcode = db_item_row[2]
            uom = db_item_row[3]
            qty = db_item_row[4]
            selling_price = db_item_row[5]
            cgst_tax_rate = db_item_row[7]
            sgst_tax_rate = db_item_row[8]
            selling_amount = float(qty) * float(selling_price)
            tax_rate = float(cgst_tax_rate) + float(sgst_tax_rate)
            tax_amount = selling_amount * tax_rate / 100
            net_amount = selling_amount + tax_amount  
            row_item.append(item_code)  
            row_item.append(barcode)  
            row_item.append(item_name)  
            row_item.append(uom)  
            row_item.append(qty)  
            row_item.append("{:.2f}".format(selling_price))  
            row_item.append("{:.2f}".format(selling_amount))  
            row_item.append("{:.2f}".format(tax_rate))  
            row_item.append("{:.2f}".format(tax_amount))  
            row_item.append("{:.2f}".format(selling_amount))  
            row_item.append("{:.2f}".format(net_amount))  
            row_item.append("{:.2f}".format(cgst_tax_rate))  
            row_item.append("{:.2f}".format(sgst_tax_rate))  
            list_items.append(row_item)
            window.Element('-TABLE-').update(values=list_items)
        sum_item_list()       
    

##############################
# Main
##############################
with open('./alignpos.json') as file_config:
  config = json.load(file_config)

kb = Controller()
list_items = []
now = datetime.datetime.now()


######
# Layout attributes
sg.theme('SystemDefault')
w, h = sg.Window.get_screen_size()
pad_button_color = 'SteelBlue3'
function_button_color = 'SteelBlue3'
disabled_text_color = 'grey32'
column_heading=['Item code', 'Barcode', 'Item Name', 'Unit', 'Qty', 'Price', 'Amount', 'Tax Rate', 'Tax', 'Net']


######
# Main window layout
layout_column_1 = [
    [
        sg.Column(
        [
            [
                sg.Text('Invoice Entry', size=(15,1) ,font=("Helvetica", 20)),
                sg.Text('User:', font=("Helvetica", 12)),
                sg.Input(key='-USERID-',readonly=True, disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89' ,default_text='admin' ,font=("Helvetica", 12),size=(15,1)),
                sg.Text('Terminal:',font=("Helvetica", 12)),
                sg.Input(key='-TERMINAL-', readonly=True ,disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89', default_text='Terminal100' ,font=("Helvetica", 12),size=(15,1)),
                sg.Text('Date:',font=("Helvetica", 12)),
                sg.Input(key='-DATE-',readonly=True ,disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89', default_text='16-apr-2021' ,font=("Helvetica", 12),size=(15,1)),
            ]
        ], size = (985,50), vertical_alignment = 'top', pad = None)    
    ],
    [
        sg.Column(
        [
            [
                sg.Text('Invoice No:', size=(8,1),  font=("Helvetica", 12)),
                sg.Input(key='-INVOICE_NO-',readonly=True, disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89' ,default_text='SINV-0010' ,font=("Helvetica", 12),size=(15,1)),
                sg.Text('Reference No:', size=(8,1),  font=("Helvetica", 12)),
                sg.Input(key='-REFERENCE_NO-',readonly=True, disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89' ,default_text='' ,font=("Helvetica", 12),size=(15,1)),
                sg.Text('Mobile No:', size=(8,1),  font=("Helvetica", 12)),
                sg.Input(key='-MOBILE_NO-',readonly=True, disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89' ,default_text='0000000000' ,font=("Helvetica", 12),size=(15,1)),
                sg.Text('UNPAID', size=(7,1),font=("Helvetica", 15)),
                sg.Button('PREV\n←', size=(8, 2), font='Calibri 12 bold', key='PREV', button_color = pad_button_color),
                sg.Button('NEXT\n→', size=(8, 2), font='Calibri 12 bold', key='NEXT', button_color = pad_button_color),    
            ]
        ], size = (985,60), vertical_alignment = 'top', pad = None)    
    ],
    [
        sg.Column(
        [
            [
                sg.Text('Barcode:', size=(8,1),  font=("Helvetica", 12)),
                sg.Input(key='-BARCODE-NB-',background_color='White',font=("Helvetica", 12),size=(15,1), enable_events = True),
                sg.Text('Item Name:', size=(8,1), font=("Helvetica", 12)),
                sg.Input(key='-ITEM_NAME-',background_color='White',font=("Helvetica", 12),size=(25,1), enable_events = True),
            ]
        ], size = (985,50), vertical_alignment = 'top', pad = None)    
    ],
    [
        sg.Column(
        [
            [
                sg.Table(values=list_items, key='-TABLE-', enable_events=True,
                     headings=column_heading,
                     font=(("Helvetica", 11)),
                     # max_col_width=500,
                     auto_size_columns=False,
                     justification='right',
                     row_height=25,
                     alternating_row_color='lightsteelBlue1',
                     num_rows=12,
                     display_row_numbers=True,
                     col_widths=[8, 15, 20, 5, 5, 10, 10, 8, 10, 10]
                     )            
            ]        
        ], size = (985,340), vertical_alignment = 'top', pad = None)    
    ],
    [
        sg.Column(
        [
            [
                sg.Button('Help\nF1', size=(13, 2), font='Helvetica 11 bold', key='F1', button_color = function_button_color),
                sg.Button('F2\nDel Item', size=(13, 2), font='Helvetica 11 bold', key='F2', button_color = function_button_color),
                sg.Button('F3\nFind Item', size=(13, 2), font='Helvetica 11 bold', key='F3', button_color = function_button_color),
                sg.Button('F4\nChange Quantity', size=(13, 2), font='Helvetica 11 bold', key='F4', button_color = function_button_color),
                sg.Button('F5\nChange Price', size=(13, 2), font='Helvetica 11 bold', key='F5', button_color = function_button_color),
                sg.Button('F6\nGet Weight', size=(13, 2), font='Helvetica 11 bold', key='F6', button_color = function_button_color)
            ],
            [
                sg.Button('F7\nNew Invoice', size=(13, 2), font='Helvetica 11 bold', key='F7', button_color = function_button_color),
                sg.Button('F8\nDelete Invoice', size=(13, 2), font='Helvetica 11 bold', key='F8', button_color = function_button_color),
                sg.Button('F9\nFind Customer', size=(13, 2), font='Helvetica 11 bold', key='F9', button_color = function_button_color),
                sg.Button('F10\nList Invoices', size=(13, 2), font='Helvetica 11 bold', key='F10', button_color = function_button_color),
                sg.Button('F11\nPrint Invoice', size=(13, 2), font='Helvetica 11 bold', key='F11', button_color = function_button_color),
                sg.Button('F12\nPayment', size=(13, 2), font='Helvetica 11 bold', key='F12', button_color = function_button_color),
                sg.Button('Esc\nExit', size=(13, 2), font='Helvetica 11 bold', key='ESC', button_color = function_button_color)
            ]               
        ], size = (985,125), background_color = 'gray80', vertical_alignment = 'top', pad = None)    
    ]       
]

layout_column_2 = [
    [
        sg.Column(
        [
            [
                sg.Image(filename = 'company-logo.GIF')
            ]
        ], size = (220,70), vertical_alignment = 'top', pad = None)    
    ],
    [
        sg.Column(
        [
            [
                sg.Text('Line Items:',  font=("Helvetica", 11) , justification="right", size=(10,1)),
                sg.Input(key='-LINE-ITEMS-', readonly=True, justification="right", disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89', default_text='0' ,font=("Helvetica", 11), size=(12,1))          
            ],
            [
                sg.Text('Total Qty:',  font=("Helvetica", 11),justification="right", size=(10,1)),
                sg.Input(key='-TOTAL-QTY-', readonly=True, justification="right", disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89', default_text='0.00' ,font=("Helvetica", 11), size=(12,1))
            ],
            [
                sg.Text('Total Price:',  font=("Helvetica", 11),justification="right", size=(10,1)),
                sg.Input(key='-TOTAL-PRICE-', readonly=True, justification="right", disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89', default_text='0.00' ,font=("Helvetica", 11),size=(12,1)),
            ],
            [
                sg.Text('CGST:', font=("Helvetica", 11),justification="right",size=(10,1), visible=False),
                sg.Input(key='-TOTAL-CGST-', readonly=True, justification="right", disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89', default_text='0.00' , font=("Helvetica", 11), size=(12,1), visible=False),
            ],
            [
                sg.Text('SGST:', font=("Helvetica", 11),justification="right",size=(10,1), visible=False),
                sg.Input(key='-TOTAL-SGST-', readonly=True, justification="right", disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89', default_text='0.00' , font=("Helvetica", 11), size=(12,1), visible=False),
            ],
            [
                sg.Text('Tax:', font=("Helvetica", 11),justification="right",size=(10,1)),
                sg.Input(key='-TOTAL-TAX-', readonly=True, justification="right", disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89', default_text='0.00' , font=("Helvetica", 11), size=(12,1)),
            ],
            [
                sg.Text('Net Price:', font=("Helvetica", 11),justification="right",size=(10,1)),
                sg.Input(key='-NET-PRICE-', readonly=True, justification="right", disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89', default_text='0.00' , font=("Helvetica", 11), size=(12,1)),
            ],
            [
                sg.Text('Discount:', font=("Helvetica", 11),justification="right",size=(10,1)),
                sg.Input(key='-DISCOUNT-', readonly=True, justification="right", disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89', default_text='0.00' , font=("Helvetica", 11), size=(12,1)),
            ],
            [
                sg.Text('Invoice Amt:', font=("Helvetica", 11),justification="right",size=(10,1)),
                sg.Input(key='-INVOICE-AMT-', readonly=True, justification="right", disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89', default_text='0.00' ,font=("Helvetica", 11),size=(12,1)),
            ],
            [
                sg.Text('Paid Amt:', font=("Helvetica", 11),justification="right",size=(10,1)),
                sg.Input(key='-PAID-AMT-', readonly=True, justification="right", disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89', default_text='0.00' , font=("Helvetica", 11), size=(12,1))
            ]            
            
        ], size = (220,220), vertical_alignment = 'top', pad = None)    
    ],
    [
        sg.Column(
        [
            [
                sg.Button('↑', size=(4, 2), font='Calibri 12 bold', key='UP', button_color = pad_button_color),
                sg.Button('7', size=(4, 2), font='Calibri 12 bold', key='T7', button_color = pad_button_color),
                sg.Button('8', size=(4, 2), font='Calibri 12 bold', key='T8', button_color = pad_button_color),
                sg.Button('9', size=(4, 2), font='Calibri 12 bold', key='T9', button_color = pad_button_color),                
                
            ],
            [
                sg.Button('↓', size=(4, 2), font='Calibri 12 bold', key='DOWN', button_color = pad_button_color),
                sg.Button('4', size=(4, 2), font='Calibri 12 bold', key='T4', button_color = pad_button_color),
                sg.Button('5', size=(4, 2), font='Calibri 12 bold', key='T5', button_color = pad_button_color),
                sg.Button('6', size=(4, 2), font='Calibri 12 bold', key='T6', button_color = pad_button_color),                  
            ],
            [
                sg.Button('→', size=(4, 2), font='Calibri 12 bold', key='RIGHT', button_color = pad_button_color),
                sg.Button('1', size=(4, 2), font='Calibri 12 bold', key='T1', button_color = pad_button_color),
                sg.Button('2', size=(4, 2), font='Calibri 12 bold', key='T2', button_color = pad_button_color),
                sg.Button('3', size=(4, 2), font='Calibri 12 bold', key='T3', button_color = pad_button_color),                
                
            ],
            [
                sg.Button('←', size=(4, 2), font='Calibri 12 bold', key='LEFT', button_color = pad_button_color),
                sg.Button('0', size=(4, 2), font='Calibri 12 bold', key='T0', button_color = pad_button_color),
                sg.Button('ENT', size=(10, 2), font='Calibri 12 bold', key='ENTER', button_color = pad_button_color),
            ],            
            [
                sg.Button('<<', size=(4, 2), font='Calibri 12 bold', key='BACK-SPACE', button_color = pad_button_color),
                sg.Button('.', size=(4, 2), font='Calibri 12 bold', key='FULL-STOP', button_color = pad_button_color),
                sg.Button('TAB', size=(10, 2), font='Calibri 12 bold', key='TAB', button_color = pad_button_color),
            ],            
        ], size = (220,280), background_color = 'gray80', vertical_alignment = 'top', pad = None)    
    ],
    [
        sg.Column(
        [
            [
                sg.Image(filename = 'align-pos-exp1.PNG')
            ]
        ], size = (220,40), vertical_alignment = 'top', pad = None)    
    ]     
]

layout_main = [
    [
        sg.Column(layout_column_1, background_color = 'gray80', size = (1000,665), vertical_alignment = 'top', pad = None),
        
        sg.Column(layout_column_2, background_color = 'gray80', size = (235,665), vertical_alignment = 'top', pad = None),        
    ]    
]

######
# Open main window
window = sg.Window('POS', layout_main,
                   font='Helvetica 11', finalize=True, location=(0,0), size=(w,h), keep_on_top=False, resizable=True,return_keyboard_events=True, use_default_focus=False
                   )
                                      
######
# Avoid focus to read only fields
window['-USERID-'].Widget.config(takefocus=0)
window['-TERMINAL-'].Widget.config(takefocus=0)
window['-DATE-'].Widget.config(takefocus=0)
window['F1'].Widget.config(takefocus=0)
window['F2'].Widget.config(takefocus=0)
window['F3'].Widget.config(takefocus=0)
window['F4'].Widget.config(takefocus=0)
window['F5'].Widget.config(takefocus=0)
window['F6'].Widget.config(takefocus=0)
window['F7'].Widget.config(takefocus=0)
window['F8'].Widget.config(takefocus=0)
window['F9'].Widget.config(takefocus=0)
window['F10'].Widget.config(takefocus=0)
window['F11'].Widget.config(takefocus=0)
window['F12'].Widget.config(takefocus=0)
window['ESC'].Widget.config(takefocus=0)
window['T1'].Widget.config(takefocus=0)
window['T2'].Widget.config(takefocus=0)
window['T3'].Widget.config(takefocus=0)
window['T4'].Widget.config(takefocus=0)
window['T5'].Widget.config(takefocus=0)
window['T6'].Widget.config(takefocus=0)
window['T7'].Widget.config(takefocus=0)
window['T8'].Widget.config(takefocus=0)
window['T9'].Widget.config(takefocus=0)
window['T0'].Widget.config(takefocus=0)
window['LEFT'].Widget.config(takefocus=0)
window['RIGHT'].Widget.config(takefocus=0)
window['ENTER'].Widget.config(takefocus=0)
window['BACK-SPACE'].Widget.config(takefocus=0)
window['FULL-STOP'].Widget.config(takefocus=0)
window['TAB'].Widget.config(takefocus=0)
window['-LINE-ITEMS-'].Widget.config(takefocus=0)
window['-TOTAL-QTY-'].Widget.config(takefocus=0)
window['-TOTAL-PRICE-'].Widget.config(takefocus=0)
window['-TOTAL-TAX-'].Widget.config(takefocus=0)
window['-NET-PRICE-'].Widget.config(takefocus=0)
window['-DISCOUNT-'].Widget.config(takefocus=0)
window['-INVOICE-AMT-'].Widget.config(takefocus=0)
window['-PAID-AMT-'].Widget.config(takefocus=0)
window['-INVOICE_NO-'].Widget.config(takefocus=0)
window['-REFERENCE_NO-'].Widget.config(takefocus=0)
window['-MOBILE_NO-'].Widget.config(takefocus=0)
window['PREV'].Widget.config(takefocus=0)
window['NEXT'].Widget.config(takefocus=0)
                   
window.Element('-BARCODE-NB-').SetFocus() 

reference_number = ''
invoice_number = ''
line_items = 0
total_qty = 0.0
total_price = 0.0
total_tax = 0.0
total_cgst = 0.0
total_sgst = 0.0
total_net_price = 0.0


######
# Load configuration parameters
db_pos_host = config["db_pos_host"]
db_pos_port = config["db_pos_port"]
db_pos_name = config["db_pos_name"]
db_pos_user = config["db_pos_user"]
db_pos_passwd = config["db_pos_passwd"]
ws_erp_user = config["ws_erp_user"]


######
# Connect to POS database
try:
    db_pos_conn = mariadb.connect(
        user = db_pos_user,
        password = db_pos_passwd,
        host = db_pos_host,
        port = db_pos_port,
        database = db_pos_name
    )
    print("POS database connected")

except mariadb.Error as db_err:
    print(f"POS database error: {db_err}")
    sys.exit(1)
    
db_pos_cur = db_pos_conn.cursor()


######
# Main window event loop
prev_event = ''
while True:
    event, values = window.read()
    print('eventm=', event,'\nvalues=',values)

    if event == sg.WIN_CLOSED:
        window.close()
        break
    if event == 'Escape:27':
        window.close()
        break
    if event == 'ESC':
        kb.press(Key.esc)
        kb.release(Key.esc)
    if event == 'TAB':
        kb.press(Key.tab)
        kb.release(Key.tab)
    if event == 'UP':
        kb.press(Key.up)
        kb.release(Key.up)
    if event == 'DOWN':
        kb.press(Key.down)
        kb.release(Key.down)
    if event == 'RIGHT':
        kb.press(Key.right)
        kb.release(Key.right)
    if event == 'LEFT':
        kb.press(Key.left)
        kb.release(Key.left)
    if event == 'BACK-SPACE':
        kb.press(Key.backspace)
        kb.release(Key.backspace)

    if event in ('T1','T2','T3','T4','T5','T6','T7','T8','T9','T0') and window.FindElementWithFocus().Key == '-BARCODE-NB-':
        inp_val = window.Element('-BARCODE-NB-').get()
        inp_val += event[1]
        window.Element('-BARCODE-NB-').update(value = inp_val)

    if event == 'FULL-STOP' and focus_element == '-BARCODE-NB-':
        inp_val = window.Element('-BARCODE-NB-').get()
        inp_val += '.'
        window.Element('-BARCODE-NB-').update(value = inp_val)

    if event in ('\t', 'TAB') and prev_event == '-BARCODE-NB-':
        proc_barcode(str(values['-BARCODE-NB-']))
         
    if event in ('\t', 'TAB') and prev_event == '-ITEM_NAME-':
        window['-TABLE-'].Widget.config(takefocus=1)
        if len(list_items) > 0:        
            table_row = window['-TABLE-'].Widget.get_children()[0]
            window['-TABLE-'].Widget.selection_set(table_row)  # move selection
            window['-TABLE-'].Widget.focus(table_row)  # move focus
            window['-TABLE-'].Widget.see(table_row)  # scroll to show i

    if event in ('F2:113', 'F2') and prev_event == '-TABLE-':
        sel_row = values['-TABLE-'][0]
        print('Selected ', sel_row)
        list_items = window.Element('-TABLE-').get()
        print('Values ', list_items[sel_row])
        list_items.pop(sel_row)
        print('Length ', len(list_items))
        if len(list_items) > 0:
            window.Element('-TABLE-').update(values=list_items)        
            window['-TABLE-'].Widget.selection_set(1)  # move selection
            window['-TABLE-'].Widget.focus(1)  # move focus
            window['-TABLE-'].Widget.see(1)  # scroll to show i  
        if len(list_items) == 0:
            window.Element('-TABLE-').update(values=[])        
            window.Element('-BARCODE-NB-').SetFocus() 
        sum_item_list()
                    
    if event in ('F4:115', 'F4') and prev_event == '-TABLE-':
        sel_row = values['-TABLE-'][0]
        print('Selected ', sel_row)
        list_items = window.Element('-TABLE-').get()
        print('Values ', list_items[sel_row])
        open_popup_chg_qty(sel_row, list_items[sel_row])
        window['-TABLE-'].Widget.config(takefocus=1)
        table_row = window['-TABLE-'].Widget.get_children()[sel_row]
        window['-TABLE-'].Widget.selection_set(table_row)  # move selection
        window['-TABLE-'].Widget.focus(table_row)  # move focus
        window['-TABLE-'].Widget.see(table_row)  # scroll to show i
        sum_item_list()

    if event in ('F7:118', 'F7'):
        save_invoice()
        clear_invoice()
        window.Element('-BARCODE-NB-').SetFocus()         

    if event in ('F8:119', 'F8'):
        delete_invoice()
        clear_invoice()
        window.Element('-BARCODE-NB-').SetFocus()         

    if event in ('Prior:33', 'PREV'):
        previous_invoice()
        window.Element('-BARCODE-NB-').SetFocus()         

    if event in ('Next:33', 'NEXT'):
        next_invoice()
        window.Element('-BARCODE-NB-').SetFocus()         

    if event in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0') and prev_event == '-BARCODE-NB-':
        proc_barcode(str(values['-BARCODE-NB-']))
    
    if event not in ('Up:38', 'Down:40', 'UP', 'DOWN', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
        prev_event = event     


######    
# Closing DB connection
db_pos_conn.close()

######
# Close Main window
window.close()
