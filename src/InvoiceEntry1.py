import PySimpleGUI as sg
import mariadb
import datetime
import json
import sys
import platform
from pynput.keyboard import Key, Controller



def isInteger(inp):
    try:
        val = int(inp)
        return True
    except ValueError:
        return False


def isFloat(inp):
    try:
        val = float(inp)
        return True
    except ValueError:
        return False

            
######
# Process Barcode field input
def proc_barcode(barcode):
    if not len(barcode) == 13:
        return
    
    if not isInteger(barcode):
        window.Element('-BARCODE-NB-').update(value='')
        window.Element('-BARCODE-NB-').set_focus()    
        return
    
    db_pos_sql_stmt = "SELECT item_code, item_name, uom, selling_price, cgst_tax_rate, sgst_tax_rate from tabItem where barcode = %s"
    db_pos_sql_data = (barcode,)
    try:
        db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
    except mariadb.Error as db_err:
        print(f"POS database error - 001: {db_err}")       
        db_pos_conn.close()
        sys.exit(1)
        
    db_item_row = db_pos_cur.fetchone()
    if db_item_row is None:
        sg.popup('Item not found',keep_on_top = True)
        window.Element('-BARCODE-NB-').update(value='')
        window.Element('-BARCODE-NB-').set_focus()    
        return

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
    row_item.append("{:.2f}".format(qty))           
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
    #window.Element('-INVOICE-AMT-').update(value="{:.2f}".format(total_net_price))
    window.Element('-TOTAL-CGST-').update(value="{:.2f}".format(total_cgst))
    window.Element('-TOTAL-SGST-').update(value="{:.2f}".format(total_sgst))


######
# Popup window for Change Quantity
def open_popup_chg_qty(row_item):
    layout_chg_qty = [
        [sg.Text(str(list_items[row_item][2]), size=(30,2),  font=("Helvetica Bold", 12))],
        [sg.Text('Existing Quantity:', size=(15,1),  font=("Helvetica", 11)),     
         sg.Input(key='-EXISTING-QTY-',readonly=True, background_color='gray89', disabled_readonly_text_color=disabled_text_color,font=("Helvetica", 11),size=(15,1))],
        [sg.Text('New Quantity:', size=(15,1),  font=("Helvetica", 11)),             
         sg.Input(key='-NEW-QTY-',readonly=False, focus=True, background_color='white',font=("Helvetica", 11),size=(15,1), enable_events=True)],
        [sg.Text('')],
        [sg.Button('Ok-F12', size=(8, 1), font='Calibri 12 bold', key='-CHG-QTY-OK-', button_color = pad_button_color),
         sg.Button('Exit-Esc', size=(8, 1), font='Calibri 12 bold', key='-CHG-QTY-ESC-', button_color = pad_button_color)]           
    ]   
    popup_chg_qty = sg.Window("Change Quantity", layout_chg_qty, location=(300,250), size=(350,180), modal=True, finalize=True,return_keyboard_events=True)
    popup_chg_qty.Element('-EXISTING-QTY-').update(value=str(list_items[row_item][4]))
    popup_chg_qty.Element('-NEW-QTY-').update(value='')
    
    while True:
        event, values = popup_chg_qty.read()
        print('eventc=', event)
        
        if event in ("Exit", '-CHG-QTY-ESC-', 'Escape:27') or event == sg.WIN_CLOSED:
            break        
        if event == "-CHG-QTY-OK-" or event == "F12:123":
            event_chg_qty_ok_clicked(popup_chg_qty, row_item)
            break
    
    popup_chg_qty.close()   


def event_chg_qty_ok_clicked(popup_chg_qty, row_item):
    applied_qty = 0
    existing_qty = popup_chg_qty.Element('-EXISTING-QTY-').get()
    applied_qty = popup_chg_qty.Element('-NEW-QTY-').get()
    if (applied_qty.isnumeric() or applied_qty.replace('.', '', 1).isdigit()):
        if float(applied_qty) == float(existing_qty):
            sg.popup('Quantity cannot be the same',keep_on_top = True)
            popup_chg_qty.Element('-NEW-QTY-').update(value='')
        else:
            tax_rate = list_items[row_item][7]
            selling_price = list_items[row_item][5]
            selling_amount = float(applied_qty) * float(selling_price)
            tax_amount = selling_amount * float(tax_rate) / 100
            net_price = selling_amount + tax_amount  
            print('applied_qty:',applied_qty)
            list_items[row_item][4] = "{:.2f}".format(float(applied_qty))
            list_items[row_item][6] = "{:.2f}".format(selling_amount)
            list_items[row_item][8] = "{:.2f}".format(tax_amount)
            list_items[row_item][9] = "{:.2f}".format(net_price)
            print('after:',row_item,':',str(list_items))
            window.Element('-TABLE-').update(values=list_items, select_rows=[row_item])


######
# Popup window for Payment
def open_popup_payment():
    layout_payment = [
        [sg.Text('Mobile No.:', size=(8,1),  font=("Helvetica", 11)),             
         sg.Input(key='-MOBILE-NO-',readonly=False, focus=True, background_color='white',font=("Helvetica", 11),size=(12,1), enable_events=True),
         sg.Input(key='-CUST-NAME-',readonly=True, focus=False, background_color='gray89', disabled_readonly_text_color=disabled_text_color,font=("Helvetica", 11),size=(25,1), enable_events=True)],
        [sg.Text('', size=(8,1))],             

        [sg.Column([
            [sg.Text('Net Amount:', size=(12,1),  font=("Helvetica", 11)),             
             sg.Input(key='-NET-AMT-',readonly=True, focus=False, background_color='gray89', disabled_readonly_text_color=disabled_text_color, font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text('Rounding Adjust:', size=(12,1),  font=("Helvetica", 11)),             
             sg.Input(key='-ROUND-ADJ-',readonly=True, focus=True, background_color='gray89', disabled_readonly_text_color=disabled_text_color, font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text('Rounded Amt:', size=(12,1),  font=("Helvetica", 11)),             
             sg.Input(key='-ROUNDED-AMT-',readonly=True, focus=True, background_color='gray89', disabled_readonly_text_color=disabled_text_color, font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text('Discount:', size=(12,1),  font=("Helvetica", 11)),             
             sg.Input(key='-DISCOUNT-AMT-',readonly=False, focus=True, background_color='white',font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text('Redeem Pts:', size=(12,1),  font=("Helvetica", 11)),             
             sg.Input(key='-REDEEM-PT-',readonly=False, focus=True, background_color='white',font=("Helvetica", 11),justification="right",size=(4,1), enable_events=True),
             sg.Text('Tot:',font=("Helvetica", 11), size=(3,1)),            
             sg.Input(key='-AVAILABLE-PT-',readonly=True, focus=True, background_color='gray89', disabled_readonly_text_color=disabled_text_color, font=("Helvetica", 11),justification="right",size=(4,1), enable_events=True)],             
            ], vertical_alignment='Top'),
        sg.Column([
            [sg.Text('Invoice Amount:', size=(12,1),  font=("Helvetica", 11)),             
             sg.Input(key='-INVOICE-AMT-',readonly=True, focus=True, background_color='gray89', disabled_readonly_text_color=disabled_text_color, font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text('Cash Payment:', size=(12,1),  font=("Helvetica", 11)),             
             sg.Input(key='-CASH-PAYMENT-',readonly=False, focus=True, background_color='white',font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True),
             sg.Text('Reference:', size=(10,1), font=("Helvetica", 11))],
            [sg.Text('Card Payment:', size=(12,1),  font=("Helvetica", 11)),             
             sg.Input(key='-CARD-PAYMENT-',readonly=False, focus=True, background_color='white',font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True),
             sg.Input(key='-CARD-REF-', focus=True, background_color='white', font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text('Credit Note:', size=(12,1),  font=("Helvetica", 11)),             
             sg.Input(key='-CREDIT-NOTE-', focus=True, background_color='white', font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True),
             sg.Input(key='-CREDIT-NOTE-REF-',readonly=False, focus=True, background_color='white',font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text('Redeem Amount:', size=(12,1),  font=("Helvetica", 11)),             
             sg.Input(key='-REDEEM-AMT-',readonly=False, focus=False, background_color='gray89', disabled_readonly_text_color=disabled_text_color,font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text('Total Payment:', size=(12,1),  font=("Helvetica", 11)),             
             sg.Input(key='-TOTAL-PAYMENT-',readonly=False, focus=False, background_color='gray89', disabled_readonly_text_color=disabled_text_color,font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text(' Balance:', size=(10,1),  font=("Helvetica bold", 14)),             
             sg.Input(key='-BALANCE-AMT-',readonly=False, focus=False, background_color='gray89', disabled_readonly_text_color=disabled_text_color,font=("Helvetica bold", 14),justification="right",size=(11,1), enable_events=True),
             sg.Button('Paid-F2', size=(7, 1), font='Calibri 12 bold', key='-PAID-', button_color = 'orange')], 
            ], vertical_alignment='Top'),
        ],
        [sg.Text('', size=(8,1))],
        [sg.Button('OK\nF12', size=(8, 2), font='Calibri 12 bold', key='-PAYMENT-OK-', button_color = pad_button_color),
         sg.Button('Exit\nEsc', size=(8, 2), font='Calibri 12 bold', key='-PAYMENT-ESC-', button_color = pad_button_color)]
    ]   

    popup_payment = sg.Window("Payment", layout_payment, location=(160,160), size=(700,350), modal=True, finalize=True,return_keyboard_events=True, keep_on_top = True)

    initialize_payment_screen(popup_payment)
    
    prev_event = ''
    while True:
        event, values = popup_payment.read()
        print('eventc=', event)
        if event in ('\t', 'TAB') and prev_event == '-DISCOUNT-AMT-':
            event_discount_entered(popup_payment)
            
        if event in ('\t', 'TAB') and prev_event == '-MOBILE-NO-':
            event_mobile_number_entered(popup_payment)       
                
        if event in ('\t', 'TAB') and prev_event == '-CASH-PAYMENT-':
            event_cash_card_payment_entered(popup_payment)       
                
        if event in ('\t', 'TAB') and prev_event == '-CARD-PAYMENT-':
            event_cash_card_payment_entered(popup_payment)       
                
        if event in ("Exit", '-PAYMENT-ESC-', 'Escape:27') or event == sg.WIN_CLOSED:
            break        
        
        if event == "-PAYMENT-OK-" or event == "F12:123":
            event_payment_ok_clicked(popup_payment)
            break
            
        if event == "-PAID-" or event == "F12:123":
            event_paid_clicked(popup_payment)

        if event not in ('Up:38', 'Down:40', 'UP', 'DOWN', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            prev_event = event     
            
    popup_payment.close()   


def initialize_payment_screen(popup_payment):
    popup_payment['-CUST-NAME-'].Widget.config(takefocus=0)
    popup_payment['-NET-AMT-'].Widget.config(takefocus=0)
    popup_payment['-INVOICE-AMT-'].Widget.config(takefocus=0)
    popup_payment['-TOTAL-PAYMENT-'].Widget.config(takefocus=0)
    popup_payment['-BALANCE-AMT-'].Widget.config(takefocus=0)
    popup_payment['-AVAILABLE-PT-'].Widget.config(takefocus=0)
    popup_payment['-REDEEM-AMT-'].Widget.config(takefocus=0)
    popup_payment['-ROUND-ADJ-'].Widget.config(takefocus=0)
    popup_payment['-ROUNDED-AMT-'].Widget.config(takefocus=0)

    net_amt = float(window.Element('-NET-PRICE-').get())
    rounding_adj = net_amt - round(net_amt, 0)
    rounded_amt = net_amt - rounding_adj
    popup_payment.Element('-NET-AMT-').update(value="{:.2f}".format(net_amt))
    popup_payment.Element('-ROUND-ADJ-').update(value="{:.2f}".format(rounding_adj))
    popup_payment.Element('-ROUNDED-AMT-').update(value="{:.2f}".format(rounded_amt))
    
    popup_payment.Element('-DISCOUNT-AMT-').update(value="{:.2f}".format(0))    
    popup_payment.Element('-INVOICE-AMT-').update(value="{:.2f}".format(rounded_amt))
    popup_payment.Element('-CASH-PAYMENT-').update(value="{:.2f}".format(rounded_amt))
    popup_payment.Element('-CARD-PAYMENT-').update(value="{:.2f}".format(0))
    popup_payment.Element('-TOTAL-PAYMENT-').update(value="{:.2f}".format(rounded_amt))
    popup_payment.Element('-BALANCE-AMT-').update(value="{:.2f}".format(0))
    popup_payment.Element('-MOBILE-NO-').SetFocus() 
    popup_payment.Element('-MOBILE-NO-').update(value='0000000000')
    
    
def event_discount_entered(popup_payment):
    rounded_amt = popup_payment.Element('-ROUNDED-AMT-').get()
    discount_amt = popup_payment.Element('-DISCOUNT-AMT-').get()
    invoice_amt = float(rounded_amt) - float(discount_amt)
    cash_payment_amt = invoice_amt
    total_payment = invoice_amt
    popup_payment.Element('-INVOICE-AMT-').update(value= "{:.2f}".format(invoice_amt)) 
    popup_payment.Element('-CASH-PAYMENT-').update(value= "{:.2f}".format(cash_payment_amt))
    popup_payment.Element('-TOTAL-PAYMENT-').update(value= "{:.2f}".format(total_payment))   
    

def event_cash_card_payment_entered(popup_payment):
    retval = 0
    retval = popup_payment.Element('-INVOICE-AMT-').get()
    retval = '0.00' if retval == '' or not retval else retval
    invoice_amt = float(retval)
    retval = popup_payment.Element('-CASH-PAYMENT-').get()
    retval = '0.00' if retval == '' or not retval else retval
    cash_payment_amt = float(retval)
    retval = popup_payment.Element('-CARD-PAYMENT-').get()
    retval = '0.00' if retval == '' or not retval else retval
    card_payment_amt = float(retval)
    if card_payment_amt > invoice_amt:
        sg.popup('Card amount cannot be more than Invoice amount',keep_on_top = True)
        return
    
    total_payment = cash_payment_amt + card_payment_amt
    balance_amt = total_payment - invoice_amt
    popup_payment.Element('-CASH-PAYMENT-').update(value= "{:.2f}".format(cash_payment_amt))   
    popup_payment.Element('-CARD-PAYMENT-').update(value= "{:.2f}".format(card_payment_amt))   
    popup_payment.Element('-INVOICE-AMT-').update(value= "{:.2f}".format(invoice_amt))   
    popup_payment.Element('-TOTAL-PAYMENT-').update(value= "{:.2f}".format(total_payment))   
    popup_payment.Element('-BALANCE-AMT-').update(value= "{:.2f}".format(balance_amt))           
    

def event_mobile_number_entered(popup_payment):
    mobile_number = popup_payment.Element('-MOBILE-NO-').get()
    if mobile_number != '':
        cust_name, loyalty_pts = get_cust_details(mobile_number)
        if cust_name != '':
            print('cust:', mobile_number, cust_name, loyalty_pts)
            popup_payment.Element('-CUST-NAME-').update(value= cust_name)
            popup_payment.Element('-AVAILABLE-PT-').update(value= loyalty_pts)            
        else:
            sg.popup('Customer not found',keep_on_top = True)
            popup_payment.Element('-MOBILE-NO-').update(value='0000000000')
            popup_payment.Element('-MOBILE-NO-').SetFocus() 


def event_payment_ok_clicked(popup_payment):
    retval = 0
    mobile_number = popup_payment.Element('-MOBILE-NO-').get()
    net_amt = float(popup_payment.Element('-NET-AMT-').get())
    retval = popup_payment.Element('-DISCOUNT-AMT-').get()
    retval = '0.00' if retval == '' or not retval else retval    
    discount_amt = float(retval)
    invoice_amt = net_amt - discount_amt
    retval = popup_payment.Element('-INVOICE-AMT-').get()
    retval = '0.00' if retval == '' or not retval else retval
    invoice_amt = float(retval)
    retval = popup_payment.Element('-CASH-PAYMENT-').get()
    retval = '0.00' if retval == '' or not retval else retval
    cash_payment_amt = float(retval)
    retval = popup_payment.Element('-CARD-PAYMENT-').get()
    retval = '0.00' if retval == '' or not retval else retval
    card_payment_amt = float(retval)
    if mobile_number == '':
        sg.popup('Mobile number is mandatory',keep_on_top = True)
        return
    if cash_payment_amt == 0 and card_payment_amt == 0:
        sg.popup('One of the Payment is mandatory',keep_on_top = True)
        return
    if card_payment_amt > invoice_amt:
        sg.popup('Card amount cannot be more than Invoice amount',keep_on_top = True)
        return       
        
    total_payment = cash_payment_amt + card_payment_amt
    balance_amt = total_payment - invoice_amt
    if balance_amt > 0:
        sg.popup('Invoice amount / Balance unpaid',keep_on_top = True)
        return

    reference_number = window.Element('-REFERENCE_NO-').get()
    retval = popup_payment.Element('-CREDIT-NOTE-').get()
    retval = '0.00' if retval == '' or not retval else retval
    credit_note_amt = float(retval)
    retval = popup_payment.Element('-REDEEM-PT-').get()
    retval = '0' if retval == '' or not retval else retval
    loyalty_points_redeemed = int(retval)
    retval = popup_payment.Element('-REDEEM-AMT-').get()
    retval = '0.00' if retval == '' or not retval else retval
    loyalty_redeemed_amt = float(retval)
    retval = popup_payment.Element('-TOTAL-PAYMENT-').get()
    retval = '0.00' if retval == '' or not retval else retval
    paid_amt = float(retval)
    

    db_pos_sql_stmt = "SELECT nextval('INVOICE_NUMBER')"
    try:
        db_pos_cur.execute(db_pos_sql_stmt)
    except mariadb.Error as db_err:
        print(f"POS database error - 002: {db_err}")       
        db_pos_conn.close()
        sys.exit(1)
            
    db_item_row = db_pos_cur.fetchone()
    if db_item_row is None:
        print('Sequence not found')
    else:
        invoice_number = db_item_row[0]
    print(invoice_number)
    
    db_pos_sql_stmt = ("UPDATE tabInvoice SET invoice_number=%s, posting_date=now(), customer=%s, discount_amount=%s, credit_note_amount=%s, loyalty_points_redeemed=%s, loyalty_redeemed_amount=%s, invoice_amount=%s, paid_amount=%s, modified=now(), modified_by=%s"
                        " WHERE name = %s")
    db_pos_sql_data = (invoice_number, mobile_number, discount_amt, credit_note_amt, loyalty_points_redeemed, loyalty_redeemed_amt, invoice_amt, paid_amt, ws_erp_user, reference_number)
    try:
        db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
    except mariadb.Error as db_err:
        print(f"POS database error - 005: {db_err}")    
        db_pos_conn.rollback()
        db_pos_conn.close()
        sys.exit(1)    

    db_pos_conn.commit()
    
    popup_payment.Element('-INVOICE-AMT-').update(value= "{:.2f}".format(invoice_amt))   
    popup_payment.Element('-TOTAL-PAYMENT-').update(value= "{:.2f}".format(total_payment))   
    popup_payment.Element('-BALANCE-AMT-').update(value= "{:.2f}".format(balance_amt))

    window.Element('-INVOICE_NO-').update(value=invoice_number)
    window.Element('-INVOICE-AMT-').update(value="{:.2f}".format(invoice_amt))
    window.Element('-DISCOUNT-').update(value="{:.2f}".format(discount_amt))
    window.Element('-PAID-AMT-').update(value="{:.2f}".format(total_payment))
    window.Element('-MOBILE_NO-').update(value=mobile_number)
    window.Element('-STATUS-').update(value='PAID', text_color = 'Green')

        
def event_paid_clicked(popup_payment):
    net_amt = float(popup_payment.Element('-NET-AMT-').get())
    retval = popup_payment.Element('-DISCOUNT-AMT-').get()
    retval = '0.00' if retval == '' or not retval else retval    
    discount_amt = float(retval)
    invoice_amt = net_amt - discount_amt
    retval = popup_payment.Element('-INVOICE-AMT-').get()
    retval = '0.00' if retval == '' or not retval else retval
    invoice_amt = float(retval)
    retval = popup_payment.Element('-CASH-PAYMENT-').get()
    retval = '0.00' if retval == '' or not retval else retval
    cash_payment_amt = float(retval)
    retval = popup_payment.Element('-CARD-PAYMENT-').get()
    retval = '0.00' if retval == '' or not retval else retval
    card_payment_amt = float(retval)
    total_payment = cash_payment_amt + card_payment_amt
    balance_amt = total_payment - invoice_amt
    if balance_amt:
        cash_payment_amt = cash_payment_amt - balance_amt
        balance_amt = 0
    total_payment = cash_payment_amt + card_payment_amt
        
    popup_payment.Element('-CASH-PAYMENT-').update(value= "{:.2f}".format(cash_payment_amt))   
    popup_payment.Element('-INVOICE-AMT-').update(value= "{:.2f}".format(invoice_amt))   
    popup_payment.Element('-TOTAL-PAYMENT-').update(value= "{:.2f}".format(total_payment))   
    popup_payment.Element('-BALANCE-AMT-').update(value= "{:.2f}".format(balance_amt))
    

def get_cust_details(mobile_number):
    customer_name = ''
    loyalty_points = 0
    db_pos_sql_stmt = "SELECT customer_name, loyalty_points from tabCustomer where mobile_number = %s"
    db_pos_sql_data = (mobile_number,)
    try:
        db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
    except mariadb.Error as db_err:
        print(f"POS database error - 001: {db_err}")       
        db_pos_conn.close()
        sys.exit(1)
            
    db_cust_row = db_pos_cur.fetchone()
    if db_cust_row is None:
        return '', 0
            
    customer_name = db_cust_row[0]
    loyalty_points = db_cust_row[1]
    return customer_name, loyalty_points


######
# Save the Invoice to DB
def save_invoice():
    invoice_number = window.Element('-INVOICE_NO-').get()
    if invoice_number != '':
        return
    reference_number = window.Element('-REFERENCE_NO-').get()
    if reference_number == '' and len(list_items) > 0:
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
        print(f"POS database error - 002: {db_err}")       
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
        print(f"POS database error - 003: {db_err}")    
        db_pos_conn.rollback()
        db_pos_conn.close()
        sys.exit(1)
    
    item_count = 0
    for row_item in list_items:
        item_count += 1
        item_code = row_item[0]
        qty = row_item[4]
        selling_price = row_item[5]
        cgst_tax_rate = row_item[10]
        sgst_tax_rate = row_item[11]
        name = reference_number + f"{item_count:04d}"
        print('InvoiceItem:', name, ':', item_code)

        db_pos_sql_stmt = ("INSERT INTO `tabInvoice Item` (name, parent, item_code, qty, standard_selling_price, applied_selling_price, cgst_tax_rate, sgst_tax_rate)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        db_pos_sql_data = (name, reference_number, item_code, qty, selling_price, selling_price, cgst_tax_rate, sgst_tax_rate)
        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error - 004: {db_err}")    
            db_pos_conn.rollback()
            db_pos_conn.close()
            sys.exit(1)            
    db_pos_conn.commit()
    window.Element('-REFERENCE_NO-').update(value=reference_number)
    


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
    print('invoice:', invoice_amount)
    
    db_pos_sql_stmt = ("UPDATE tabInvoice SET posting_date=now(), customer=%s, total_amount=%s, cgst_tax_amount=%s, sgst_tax_amount=%s, invoice_amount=%s, terminal_id=%s, creation=now(), owner=%s"
                        " WHERE name = %s")
    db_pos_sql_data = (mobile_number, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, terminal_id, ws_erp_user, reference_number)
    try:
        db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
    except mariadb.Error as db_err:
        print(f"POS database error - 005: {db_err}")    
        db_pos_conn.rollback()
        db_pos_conn.close()
        sys.exit(1)
    db_pos_sql_stmt = ("DELETE FROM `tabInvoice Item` WHERE parent = '" + reference_number + "'")
    
    try:
        db_pos_cur.execute(db_pos_sql_stmt)
    except mariadb.Error as db_err:
        print(f"POS database error - 006: {db_err}")    
        db_pos_conn.rollback()
        db_pos_conn.close()
        sys.exit(1)
    print('here2')
 
    item_count = 0
    for row_item in list_items:
        item_count += 1
        item_code = row_item[0]
        qty = row_item[4]
        selling_price = row_item[5]
        cgst_tax_rate = row_item[10]
        sgst_tax_rate = row_item[11]
        name = reference_number + f"{item_count:04d}"
        print('updating InvoiceItem:', name, ':', item_code)

        db_pos_sql_stmt = ("INSERT INTO `tabInvoice Item` (name, parent, item_code, qty, standard_selling_price, applied_selling_price, cgst_tax_rate, sgst_tax_rate)"
                            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
        db_pos_sql_data = (name, reference_number, item_code, qty, selling_price, selling_price, cgst_tax_rate, sgst_tax_rate)
        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error - 007: {db_err}")    
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
        print(f"POS database error - 008: {db_err}")    
        db_pos_conn.rollback()
        db_pos_conn.close()
        sys.exit(1)

    db_pos_sql_stmt = ("DELETE FROM `tabInvoice` WHERE name = '" + reference_number + "'")
    try:
        db_pos_cur.execute(db_pos_sql_stmt)
    except mariadb.Error as db_err:
        print(f"POS database error - 009: {db_err}")    
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
    discount_amt = 0
    total_cgst  = 0
    total_sgst  = 0
    total_payment = 0
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
    window.Element('-DISCOUNT-').update(value="{:.2f}".format(discount_amt))
    window.Element('-PAID-AMT-').update(value="{:.2f}".format(total_payment))    
    window.Element('-TABLE-').update(values=list_items)     
    window.Element('-INVOICE_NO-').update(value='')
    window.Element('-REFERENCE_NO-').update(value='')
    window.Element('-MOBILE_NO-').update(value='0000000000')
    window.Element('-STATUS-').update(value='UNPAID', text_color = 'Red')

    
def goto_previous_invoice():
    print('prev')
    reference_number = window.Element('-REFERENCE_NO-').get()
    if (reference_number == ''):
        db_pos_sql_stmt = ("SELECT name, invoice_number, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, discount_amount, paid_amount from tabInvoice WHERE name = (select max(name) from tabInvoice)")
        try:
            db_pos_cur.execute(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error - 010: {db_err}")       
            db_pos_conn.close()
            sys.exit(1)
    else:
        db_pos_sql_stmt = ("SELECT name, invoice_number, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, discount_amount, paid_amount from tabInvoice WHERE name = (select max(name) from tabInvoice where name < %s)")
        db_pos_sql_data = (reference_number,)

        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error - 011: {db_err}")       
            db_pos_conn.close()
            sys.exit(1)
    
    db_invoice_row = db_pos_cur.fetchone()
    if db_invoice_row is None:
        print('Invoice not found')
    else:
        window.Element('-REFERENCE_NO-').update(value= '')
        window.Element('-INVOICE_NO-').update(value= '')
        window.Element('-MOBILE_NO-').update(value= '')
        window.Element('-STATUS-').update(value= 'UNPAID', text_color = 'Red')       
        reference_number = db_invoice_row[0]
        window.Element('-REFERENCE_NO-').update(value= reference_number)
        invoice_number = db_invoice_row[1]
        window.Element('-INVOICE_NO-').update(value= invoice_number)       
        mobile_number = db_invoice_row[2]
        
        retval = db_invoice_row[6]
        retval = '0.00' if retval == '' or not retval else retval
        invoice_amount = float(retval)
        
        retval = db_invoice_row[7]
        retval = '0.00' if retval == '' or not retval else retval
        discount_amount = float(retval)

        retval = db_invoice_row[8]
        retval = '0.00' if retval == '' or not retval else retval        
        paid_amount = float(retval)
        
        window.Element('-MOBILE_NO-').update(value= mobile_number)
        if invoice_number:
            window.Element('-STATUS-').update(value= 'PAID', text_color = 'Lime Green')   
        else:
            window.Element('-STATUS-').update(value= 'UNPAID', text_color = 'Red')
        window.Element('-DISCOUNT-').update(value= "{:.2f}".format(discount_amount))
        window.Element('-INVOICE-AMT-').update(value= "{:.2f}".format(invoice_amount))       
        window.Element('-PAID-AMT-').update(value= "{:.2f}".format(paid_amount))            

        db_pos_sql_stmt = ("SELECT inv_item.item_code, item_name, barcode, uom, qty,standard_selling_price, applied_selling_price, inv_item.cgst_tax_rate,inv_item.sgst_tax_rate from `tabInvoice Item` inv_item, tabItem item WHERE inv_item.parent = %s and inv_item.item_code = item.item_code")
        db_pos_sql_data = (reference_number,)
        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error - 012: {db_err}")       
            db_pos_conn.close()
            sys.exit(1)
            
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
            print('price:', selling_price)
            cgst_tax_rate = db_item_row[7]
            sgst_tax_rate = db_item_row[8]
            selling_amount = float(qty) * float(selling_price)
            tax_rate = float(cgst_tax_rate) + float(sgst_tax_rate)
            tax_amount = selling_amount * tax_rate / 100
            net_amount = selling_amount + tax_amount  
            row_item = []
            row_item.append(item_code)  
            row_item.append(barcode)  
            row_item.append(item_name)  
            row_item.append(uom)  
            row_item.append("{:.2f}".format(qty))  
            row_item.append("{:.2f}".format(selling_price))  
            row_item.append("{:.2f}".format(selling_amount))  
            row_item.append("{:.2f}".format(tax_rate))  
            row_item.append("{:.2f}".format(tax_amount))  
            row_item.append("{:.2f}".format(net_amount))  
            row_item.append("{:.2f}".format(cgst_tax_rate))  
            row_item.append("{:.2f}".format(sgst_tax_rate))  
            list_items.append(row_item)
            window.Element('-TABLE-').update(values=list_items)

        sum_item_list()


def goto_next_invoice():
    print('next')
    reference_number = window.Element('-REFERENCE_NO-').get()
    if (reference_number == ''):
        return
    else:
        db_pos_sql_stmt = ("SELECT name, invoice_number, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, discount_amount, paid_amount from tabInvoice WHERE name = (select min(name) from tabInvoice where name > %s)")
        db_pos_sql_data = (reference_number,)

        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error - 013: {db_err}")       
            db_pos_conn.close()
            sys.exit(1)
    
    db_invoice_row = db_pos_cur.fetchone()
    if db_invoice_row is None:
        print('Invoice not found')
    else:
        window.Element('-REFERENCE_NO-').update(value= '')
        window.Element('-INVOICE_NO-').update(value= '')
        window.Element('-MOBILE_NO-').update(value= '')   
        window.Element('-STATUS-').update(value= 'UNPAID', text_color = 'Red')               
        reference_number = db_invoice_row[0]
        window.Element('-REFERENCE_NO-').update(value= reference_number)
        invoice_number = db_invoice_row[1]
        window.Element('-INVOICE_NO-').update(value= invoice_number)        
        mobile_number = db_invoice_row[2]
        
        retval = db_invoice_row[6]
        retval = '0.00' if retval == '' or not retval else retval
        invoice_amount = float(retval)
        
        retval = db_invoice_row[7]
        retval = '0.00' if retval == '' or not retval else retval
        discount_amount = float(retval)

        retval = db_invoice_row[8]
        retval = '0.00' if retval == '' or not retval else retval        
        paid_amount = float(retval)
        
        window.Element('-MOBILE_NO-').update(value= mobile_number)
        if invoice_number:
            window.Element('-STATUS-').update(value= 'PAID', text_color = 'Lime Green')   
        else:
            window.Element('-STATUS-').update(value= 'UNPAID', text_color = 'Red')
        window.Element('-DISCOUNT-').update(value= "{:.2f}".format(discount_amount))
        window.Element('-INVOICE-AMT-').update(value= "{:.2f}".format(invoice_amount))       
        window.Element('-PAID-AMT-').update(value= "{:.2f}".format(paid_amount))            

        db_pos_sql_stmt = ("SELECT inv_item.item_code, item_name, barcode, uom, qty,standard_selling_price, applied_selling_price, inv_item.cgst_tax_rate,inv_item.sgst_tax_rate from `tabInvoice Item` inv_item, tabItem item WHERE inv_item.parent = %s and inv_item.item_code = item.item_code")
        db_pos_sql_data = (reference_number,)
        print(db_pos_sql_stmt)
        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error - 014: {db_err}")       
            db_pos_conn.close()
            sys.exit(1)
            
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
            print('price:', selling_price, ' ', db_item_row[5])
            
            cgst_tax_rate = db_item_row[7]
            sgst_tax_rate = db_item_row[8]
            selling_amount = float(qty) * float(selling_price)
            tax_rate = float(cgst_tax_rate) + float(sgst_tax_rate)
            tax_amount = selling_amount * tax_rate / 100
            net_amount = selling_amount + tax_amount  
            row_item = []            
            row_item.append(item_code)  
            row_item.append(barcode)  
            row_item.append(item_name)  
            row_item.append(uom)  
            row_item.append("{:.2f}".format(qty))  
            row_item.append("{:.2f}".format(selling_price))
            row_item.append("{:.2f}".format(selling_amount))  
            row_item.append("{:.2f}".format(tax_rate))  
            row_item.append("{:.2f}".format(tax_amount))  
            row_item.append("{:.2f}".format(net_amount))  
            row_item.append("{:.2f}".format(cgst_tax_rate))  
            row_item.append("{:.2f}".format(sgst_tax_rate)) 
            list_items.append(row_item)
            window.Element('-TABLE-').update(values=list_items)
        sum_item_list()       
    
def goto_last_invoice():
    print('last')
    db_pos_sql_stmt = ("SELECT name, invoice_number, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, discount_amount, paid_amount from tabInvoice WHERE name = (select max(name) from tabInvoice)")

    try:
        db_pos_cur.execute(db_pos_sql_stmt)
    except mariadb.Error as db_err:
        print(f"POS database error - 015: {db_err}")       
        db_pos_conn.close()
        sys.exit(1)
    
    db_invoice_row = db_pos_cur.fetchone()
    if db_invoice_row is None:
        print('Invoice not found')
    else:
        window.Element('-REFERENCE_NO-').update(value= '')
        window.Element('-INVOICE_NO-').update(value= '')
        window.Element('-MOBILE_NO-').update(value= '')   
        window.Element('-STATUS-').update(value= 'UNPAID', text_color = 'Red')               
        reference_number = db_invoice_row[0]
        window.Element('-REFERENCE_NO-').update(value= reference_number)
        invoice_number = db_invoice_row[1]
        window.Element('-INVOICE_NO-').update(value= invoice_number)        
        mobile_number = db_invoice_row[2]
        
        retval = db_invoice_row[6]
        retval = '0.00' if retval == '' or not retval else retval
        invoice_amount = float(retval)
        
        retval = db_invoice_row[7]
        retval = '0.00' if retval == '' or not retval else retval
        discount_amount = float(retval)

        retval = db_invoice_row[8]
        retval = '0.00' if retval == '' or not retval else retval        
        paid_amount = float(retval)
        
        window.Element('-MOBILE_NO-').update(value= mobile_number)
        if invoice_number:
            window.Element('-STATUS-').update(value= 'PAID', text_color = 'Lime Green')   
        else:
            window.Element('-STATUS-').update(value= 'UNPAID', text_color = 'Red')
        window.Element('-DISCOUNT-').update(value= "{:.2f}".format(discount_amount))
        window.Element('-INVOICE-AMT-').update(value= "{:.2f}".format(invoice_amount))       
        window.Element('-PAID-AMT-').update(value= "{:.2f}".format(paid_amount))            

        db_pos_sql_stmt = ("SELECT inv_item.item_code, item_name, barcode, uom, qty,standard_selling_price, applied_selling_price, inv_item.cgst_tax_rate,inv_item.sgst_tax_rate from `tabInvoice Item` inv_item, tabItem item WHERE inv_item.parent = %s and inv_item.item_code = item.item_code")
        db_pos_sql_data = (reference_number,)
        print(db_pos_sql_stmt)
        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error - 016: {db_err}")       
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
            print(tax_rate, cgst_tax_rate, sgst_tax_rate)
            tax_amount = selling_amount * tax_rate / 100
            net_amount = selling_amount + tax_amount  
            row_item = []
            row_item.append(item_code)  
            row_item.append(barcode)  
            row_item.append(item_name)  
            row_item.append(uom)  
            row_item.append("{:.2f}".format(qty))  
            row_item.append("{:.2f}".format(selling_price))  
            row_item.append("{:.2f}".format(selling_amount))  
            row_item.append("{:.2f}".format(tax_rate))  
            row_item.append("{:.2f}".format(tax_amount))  
            row_item.append("{:.2f}".format(net_amount))  
            row_item.append("{:.2f}".format(cgst_tax_rate))  
            row_item.append("{:.2f}".format(sgst_tax_rate))  
            list_items.append(row_item)
            window.Element('-TABLE-').update(values=list_items)
        sum_item_list()       


def goto_first_invoice():
    print('first')
    db_pos_sql_stmt = ("SELECT name, invoice_number, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, discount_amount, paid_amount from tabInvoice WHERE name = (select min(name) from tabInvoice)")

    try:
        db_pos_cur.execute(db_pos_sql_stmt)
    except mariadb.Error as db_err:
        print(f"POS database error - 017: {db_err}")       
        db_pos_conn.close()
        sys.exit(1)
    
    db_invoice_row = db_pos_cur.fetchone()
    if db_invoice_row is None:
        print('Invoice not found')
    else:
        window.Element('-REFERENCE_NO-').update(value= '')
        window.Element('-INVOICE_NO-').update(value= '')
        window.Element('-MOBILE_NO-').update(value= '')

        reference_number = db_invoice_row[0]
        invoice_number = db_invoice_row[1]
        mobile_number = db_invoice_row[2]
        
        retval = db_invoice_row[6]
        retval = '0.00' if retval == '' or not retval else retval
        invoice_amount = float(retval)
        
        retval = db_invoice_row[7]
        retval = '0.00' if retval == '' or not retval else retval
        discount_amount = float(retval)

        retval = db_invoice_row[8]
        retval = '0.00' if retval == '' or not retval else retval        
        paid_amount = float(retval)
        
        window.Element('-REFERENCE_NO-').update(value= reference_number)
        window.Element('-INVOICE_NO-').update(value= invoice_number)       
        window.Element('-MOBILE_NO-').update(value= mobile_number)
        if invoice_number:
            window.Element('-STATUS-').update(value= 'PAID', text_color = 'Lime Green')   
        else:
            window.Element('-STATUS-').update(value= 'UNPAID', text_color = 'Red')
        window.Element('-DISCOUNT-').update(value= "{:.2f}".format(discount_amount))
        window.Element('-INVOICE-AMT-').update(value= "{:.2f}".format(invoice_amount))       
        window.Element('-PAID-AMT-').update(value= "{:.2f}".format(paid_amount))            
        
        db_pos_sql_stmt = ("SELECT inv_item.item_code, item_name, barcode, uom, qty,standard_selling_price, applied_selling_price, inv_item.cgst_tax_rate, inv_item.sgst_tax_rate from `tabInvoice Item` inv_item, tabItem item WHERE inv_item.parent = %s and inv_item.item_code = item.item_code")
        db_pos_sql_data = (reference_number,)
        print(db_pos_sql_stmt)
        try:
            db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error - 018: {db_err}")       
            db_pos_conn.close()
            sys.exit(1)
            
        db_items = db_pos_cur.fetchall()
        row_item = []
        list_items.clear()
        
        for db_item_row in db_items:
            print('\ndb_item_row:', db_item_row)
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
            row_item = []
            row_item.append(item_code)  
            row_item.append(barcode)  
            row_item.append(item_name)  
            row_item.append(uom)  
            row_item.append("{:.2f}".format(qty))  
            row_item.append("{:.2f}".format(selling_price))  
            row_item.append("{:.2f}".format(selling_amount))  
            row_item.append("{:.2f}".format(tax_rate))  
            row_item.append("{:.2f}".format(tax_amount))  
            row_item.append("{:.2f}".format(net_amount))  
            row_item.append("{:.2f}".format(cgst_tax_rate))  
            row_item.append("{:.2f}".format(sgst_tax_rate))  
            print('\nrow_item:', row_item)

            list_items.append(row_item)
        window.Element('-TABLE-').update(values=list_items)
        print('\nlist_items:', list_items)
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
                sg.Input(key='-INVOICE_NO-',readonly=True, disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89' ,default_text='' ,font=("Helvetica", 12),size=(10,1)),
                sg.Text('Reference No:', size=(8,1),  font=("Helvetica", 12)),
                sg.Input(key='-REFERENCE_NO-',readonly=True, disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89' ,default_text='' ,font=("Helvetica", 12),size=(10,1)),
                sg.Text('Mobile No:', size=(8,1),  font=("Helvetica", 12)),
                sg.Input(key='-MOBILE_NO-',readonly=True, disabled_readonly_text_color=disabled_text_color, disabled_readonly_background_color='gray89' ,default_text='' ,font=("Helvetica", 12),size=(15,1)),
                sg.Text(key='-STATUS-', size=(7,1),font=("Helvetica", 15)),
                sg.Button('BEGN\nHome', size=(6, 2), font='Calibri 12 bold', key='BEGN', button_color = pad_button_color),
                sg.Button('PREV\nPgUp', size=(6, 2), font='Calibri 12 bold', key='PREV', button_color = pad_button_color),
                sg.Button('NEXT\nPgDn', size=(6, 2), font='Calibri 12 bold', key='NEXT', button_color = pad_button_color),    
                sg.Button('END\nEnd', size=(6, 2), font='Calibri 12 bold', key='END', button_color = pad_button_color),    
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
                     col_widths=[10, 15, 20, 5, 5, 10, 10, 8, 10, 10]
                     )            
            ]        
        ], size = (985,340), vertical_alignment = 'top', pad = None)    
    ],
    [
        sg.Column(
        [
            [
                sg.Button('Help\nF1', size=(13, 2), font='Helvetica 11 bold', key='F1', button_color = function_button_color),
                sg.Button('Del Item\nF2', size=(13, 2), font='Helvetica 11 bold', key='F2', button_color = function_button_color),
                sg.Button('Find Item\nF3', size=(13, 2), font='Helvetica 11 bold', key='F3', button_color = function_button_color),
                sg.Button('Change Quantity\nF4', size=(13, 2), font='Helvetica 11 bold', key='F4', button_color = function_button_color),
                sg.Button('Change Price\nF5', size=(13, 2), font='Helvetica 11 bold', key='F5', button_color = function_button_color),
                sg.Button('Get Weight\nF6', size=(13, 2), font='Helvetica 11 bold', key='F6', button_color = function_button_color)
            ],
            [
                sg.Button('New Invoice\nF7', size=(13, 2), font='Helvetica 11 bold', key='F7', button_color = function_button_color),
                sg.Button('Delete Invoice\nF8', size=(13, 2), font='Helvetica 11 bold', key='F8', button_color = function_button_color),
                sg.Button('Find Customer\nF9', size=(13, 2), font='Helvetica 11 bold', key='F9', button_color = function_button_color),
                sg.Button('List Invoices\nF10', size=(13, 2), font='Helvetica 11 bold', key='F10', button_color = function_button_color),
                sg.Button('Print Invoice\nF11', size=(13, 2), font='Helvetica 11 bold', key='F11', button_color = function_button_color),
                sg.Button('Payment\nF12', size=(13, 2), font='Helvetica 11 bold', key='F12', button_color = function_button_color),
                sg.Button('Exit\nEsc', size=(13, 2), font='Helvetica 11 bold', key='ESC', button_color = function_button_color)
            ]               
        ], size = (985,125), background_color = 'gray80', vertical_alignment = 'top', pad = None)    
    ]       
]

layout_column_2 = [
    [
        sg.Column(
        [
            [
                sg.Image(filename = 'al-fareeda-logo.PNG')
            ]
        ], size = (140,70), vertical_alignment = 'top', pad=(45,5))    
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
                sg.Text('Total Amount:',  font=("Helvetica", 11),justification="right", size=(10,1)),
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
                sg.Text('Net Amount:', font=("Helvetica", 11),justification="right",size=(10,1)),
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

######
# Set focus to Barcode (first field)                   
window.Element('-BARCODE-NB-').SetFocus() 
window.Element('-STATUS-').update(value='UNPAID', text_color = 'Red') 


######
# Initialize Bind Variables                   
reference_number = ''
invoice_number = ''
line_items = 0
total_qty = 0.0
total_price = 0.00
total_tax = 0.00
total_cgst = 0.00
total_sgst = 0.00
total_net_price = 0.00
list_items.clear()
row_item = []


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
    print(f"POS database error - 019: {db_err}")
    sys.exit(1)
    
db_pos_cur = db_pos_conn.cursor()


######
# Main window event loop
prev_event = ''
while True:
    event, values = window.read()
    #print('eventm=', event,'\nvalues=',values)
    print('eventm=', event)

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

    '''
    if event == 'FULL-STOP' and focus_element == '-BARCODE-NB-':
        inp_val = window.Element('-BARCODE-NB-').get()
        inp_val += '.'
        window.Element('-BARCODE-NB-').update(value = inp_val)
    '''
    
    if event in ('\t', 'TAB') and prev_event == '-BARCODE-NB-':
        invoice_number = window.Element('-INVOICE_NO-').get()       
        if invoice_number == '':    
            proc_barcode(str(values['-BARCODE-NB-']))
         
    if event in ('\t', 'TAB') and prev_event == '-ITEM_NAME-':
        window['-TABLE-'].Widget.config(takefocus=1)
        if len(list_items) > 0:        
            table_row = window['-TABLE-'].Widget.get_children()[0]
            window['-TABLE-'].Widget.selection_set(table_row)  # move selection
            window['-TABLE-'].Widget.focus(table_row)  # move focus
            window['-TABLE-'].Widget.see(table_row)  # scroll to show i

    if event in ('F2:113', 'F2') and prev_event == '-TABLE-':
        invoice_number = window.Element('-INVOICE_NO-').get()       
        if invoice_number == '':   
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
        invoice_number = window.Element('-INVOICE_NO-').get()   
        if invoice_number == '':
            sel_row = values['-TABLE-'][0]
            list_items = window.Element('-TABLE-').get()
            print('initial:',row_item,':',str(list_items))
            open_popup_chg_qty(sel_row)
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
        invoice_number = window.Element('-INVOICE_NO-').get()       
        if invoice_number == '':  
            confirm_delete = sg.popup_ok_cancel('Invoice will be Deleted',keep_on_top = True)
            if confirm_delete == 'OK':
                delete_invoice()
                clear_invoice()
                window.Element('-BARCODE-NB-').SetFocus()         

    if event in ('F12:123', 'F12'):
        invoice_number = window.Element('-INVOICE_NO-').get()  
        line_items = window.Element('-LINE-ITEMS-').get()  
        if invoice_number == '' and int(line_items) > 0:
            save_invoice()
            open_popup_payment()
            window.Element('-BARCODE-NB-').SetFocus()         
            
    if event in ('Home:36', 'BEGN'):
        save_invoice()
        goto_first_invoice()
        window.Element('-BARCODE-NB-').SetFocus()         

    if event in ('Prior:33', 'PREV'):
        save_invoice()
        goto_previous_invoice()
        window.Element('-BARCODE-NB-').SetFocus()         

    if event in ('Next:33', 'NEXT'):
        save_invoice()
        goto_next_invoice()
        window.Element('-BARCODE-NB-').SetFocus()         

    if event in ('End:35', 'END'):
        save_invoice()
        goto_last_invoice()
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
