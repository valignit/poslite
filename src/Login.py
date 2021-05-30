import PySimpleGUI as sg
import json
import sys
from DBOperations import DBOperations
from loginLayout import loginLayout
import platform
from datetime import date
import tkinter as tk
from tkinter import *
from InvoiceLayout import InvoiceLayout
from pynput.keyboard import Key, Controller

def exitPos():
    print('Exit Pos')

def login():
    print('login Pos')

with open('alignpos.json') as f:
    data = json.load(f)

db_pos_host = data['db_pos_host']
db_pos_port = data['db_pos_port']
db_pos_name = data['db_pos_name']
db_pos_user = data['db_pos_user']
db_pos_passwd = data['db_pos_passwd']

#dbManager =    dbManager(dbHost, dbPort, dbName, dbUser, dbPwd)
dbOperation = DBOperations(db_pos_host,db_pos_port,db_pos_name,db_pos_user,db_pos_passwd)

heading: dict = {'size':(100, 1), 'font':('Helvetica 20 bold'), 'text_color':'blue'}
txt_font: dict = {'font':('Helvetica 11 bold'), 'justification':'right', 'size':(10, 1), 'text_color':'black'}
input_fld: dict = {'readonly':'True', 'disabled_readonly_text_color':'gray','disabled_readonly_background_color':'gray89','size':(20, 1)}

loginLayout = loginLayout()

header = loginLayout.header()
footer = loginLayout.footer()
buttonLayout = loginLayout.loginButtons()

navigationWindow = None

def open_popup_chg_qty(row_item, list_item):
    layout_chg_qty = [
        [sg.Text(str(list_item[2]), size=(30, 2), font=("Helvetica Bold", 12))],
        [sg.Text('Existing Quantity:', size=(15, 1), font=("Helvetica", 11)),
         sg.Input(key='-EXISTING-QTY-', readonly=True, background_color='gray89',
                  disabled_readonly_text_color=InvoiceLayout.disabled_text_color, font=("Helvetica", 11), size=(15, 1))],
        [sg.Text('New Quantity:', size=(15, 1), font=("Helvetica", 11)),
         sg.Input(key='-NEW-QTY-', readonly=False, focus=True, background_color='white', font=("Helvetica", 11),
                  size=(15, 1), enable_events=True)],
        [sg.Text('')],
        [sg.Button('F12-Ok', size=(8, 1), font='Calibri 12 bold', key='-CHG-QTY-OK-', button_color=InvoiceLayout.pad_button_color),
         sg.Button('Esc-Exit', size=(8, 1), font='Calibri 12 bold', key='-CHG-QTY-ESC-', button_color=InvoiceLayout.pad_button_color)]
    ]

    popup_chg_qty = sg.Window("Change Quantity", layout_chg_qty, location=(300, 250), size=(350, 180), modal=True,
                              finalize=True, return_keyboard_events=True)
    popup_chg_qty.Element('-EXISTING-QTY-').update(value=str(list_item[4]))

    while True:
        event, values = popup_chg_qty.read()
        print('eventc=', event)

        if event in ("Exit", '-CHG-QTY-ESC-', 'Escape:27') or event == sg.WIN_CLOSED:
            break
        if event == "-CHG-QTY-OK-" or event == "F12:123":
            applied_qty = popup_chg_qty.Element('-NEW-QTY-').get()
            if (applied_qty.isnumeric() or applied_qty.replace('.', '', 1).isdigit()):
                tax_rate = InvoiceLayout.list_items[row_item][7]
                selling_price = InvoiceLayout.list_items[row_item][6]
                selling_amount = float(applied_qty) * float(selling_price)
                tax_amount = selling_amount * float(tax_rate) / 100
                net_price = selling_amount + tax_amount
                InvoiceLayout.list_items[row_item][4] = applied_qty
                InvoiceLayout.list_items[row_item][6] = "{:.2f}".format(selling_amount)
                InvoiceLayout.list_items[row_item][8] = "{:.2f}".format(tax_amount)
                InvoiceLayout.list_items[row_item][9] = "{:.2f}".format(net_price)
                window.Element('-TABLE-').update(values=InvoiceLayout.list_items, select_rows=[row_item])
                # sum_item_list()
                break

    popup_chg_qty.close()


def sum_item_list():
    line_items = 0
    total_qty = 0.0
    total_price = 0.0
    total_tax = 0.0
    total_net_price = 0.0

    for row_item in InvoiceLayout.list_items:
        line_items += 1
        total_qty += float(row_item[4])
        total_price += float(row_item[6])
        total_tax += float(row_item[8])
        total_net_price += float(row_item[9])

    window.Element('-LINE-ITEMS-').update(value=str(line_items))
    window.Element('-TOTAL-QTY-').update(value="{:.2f}".format(total_qty))
    window.Element('-TOTAL-PRICE-').update(value="{:.2f}".format(total_price))
    window.Element('-TOTAL-TAX-').update(value="{:.2f}".format(total_tax))
    window.Element('-NET-PRICE-').update(value="{:.2f}".format(total_net_price))
    window.Element('-INVOICE-AMT-').update(value="{:.2f}".format(total_net_price))

def proc_barcode(barcode):

    if len(barcode) > 12:
        print('barcode=', barcode)
        #db_pos_cur.execute("SELECT item_code, item_name, uom, selling_price, cgst_tax_rate, sgst_tax_rate from tabItem where barcode = '" + barcode + "'")
        #db_item_row = db_pos_cur.fetchone()
        db_item_row = 1
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
            print(item_name)
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
            InvoiceLayout.list_items.append(row_item)
            print(InvoiceLayout.list_items)
            window.Element('-TABLE-').update(values=InvoiceLayout.list_items)
            window.Element('-BARCODE-NB-').update(value='')
            window.Element('-BARCODE-NB-').set_focus()
            sum_item_list()


def invoiceEntry():
    kb = Controller()
    w, h = sg.Window.get_screen_size()
    win_w = w
    win_h = h
    invWindow = sg.Window('POS', InvoiceLayout.layout_main,
                       font='Helvetica 11', finalize=True, location=(0, 0), size=(win_w, win_h), keep_on_top=True,
                       resizable=True, return_keyboard_events=True, use_default_focus=False
                       )

    prev_event = ''
    focus_element = ''
    while True:
        event, values = invWindow.read()
        print('eventm=', event, '\nvalues=', values)
        # print('eventm=', event, ' prev=', prev_event, ' focus=', str(focus_element))

        if event == sg.WIN_CLOSED:
            invWindow.close()
            break
        if event == 'Escape:27':
            invWindow.close()
            navigationWindow.UnHide()
            window['-LOGINUSER-'].update('')
            window['-LOGINPWD-'].update('')
            window.Element('-LOGINUSER-').set_focus()
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

        if event in ('T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9',
                     'T0') and window.FindElementWithFocus().Key == '-BARCODE-NB-':
            inp_val = window.Element('-BARCODE-NB-').get()
            inp_val += event[1]
            window.Element('-BARCODE-NB-').update(value=inp_val)

        if event == 'FULL-STOP' and focus_element == '-BARCODE-NB-':
            inp_val = window.Element('-BARCODE-NB-').get()
            inp_val += '.'
            window.Element('-BARCODE-NB-').update(value=inp_val)

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

        if event in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0') and prev_event == '-BARCODE-NB-':
            proc_barcode(str(values['-BARCODE-NB-']))

        if event not in ('Up:38', 'Down:40', 'UP', 'DOWN', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            prev_event = event



def navigation():
    navigationMenu = loginLayout.navigationMenu()
    navigationWindow = sg.Window('Navigation Window', navigationMenu, enable_close_attempted_event=True, no_titlebar=True, keep_on_top=True,size=(350, 500), return_keyboard_events=True, finalize=True)

    navigationWindow.bind('<Escape>', exitPos())
    navigationWindow.bind('<F1>', '')
    navigationWindow.bind('<F2>', '')
    navigationWindow.bind('<F3>', '')
    navigationWindow.bind('<F4>', '')

    while True:             # Event Loop
        event, values = navigationWindow.Read()
        print("event",event)
        if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event is None or event == sg.WIN_CLOSED:
            sys.exit(0)

        if event == '-SignOut-' or event == '<Escape>':
            navigationWindow.hide()
            window.UnHide()
            window['-LOGINUSER-'].update('')
            window['-LOGINPWD-'].update('')
            window.Element('-LOGINUSER-').set_focus()
            break

        if event == '-Invoice-' or event == '<F2>':
            print('invoice screen')
            navigationWindow.hide()
            invoiceEntry()
    navigationWindow.Close()



layout = [
    [header],
    [sg.Text(' ', key='ErrMsg', size=(100, 1))],
    [sg.Text('User Name:', **txt_font,pad=((20, 5), (10, 0))),
     sg.In(key='-LOGINUSER-', focus=True,pad=((0, 0), (15, 5)), size=(20, 4))],
    [sg.Text('Password:',**txt_font ,pad=((20, 5), (10, 0))),
     sg.In(key='-LOGINPWD-' ,password_char='*', pad=((0, 0), (15, 0)), size=(20, 4))],
    [sg.Text('Terminal:',**txt_font ,pad=((20, 5), (10, 0))),
     sg.In(key='-TERMINAL-', default_text=data['terminal_id'],**input_fld , pad=((0, 0), (15, 5)))],
    [buttonLayout],
    [footer]
]

window = sg.Window('Login Window', layout, enable_close_attempted_event=True,no_titlebar=True,keep_on_top=True, size=(350, 450), return_keyboard_events=True,finalize=True)

window.bind('<Escape>', exitPos())
window.bind('<F12>', login())
window.Element('-LOGINUSER-').set_focus()

while True:
    event, values = window.read()
    #print(event, values)
    if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit?',title='Confirmation', keep_on_top=True) == 'Yes':
            break
    if event == '<Escape>':
        if sg.popup_yes_no('Do you want to Exit?',title='Confirmation', keep_on_top=True) == 'Yes':
            break
    if event == '<F12>' or event == '-LoginOk-' or event == '<Enter>':
        uid = window['-LOGINUSER-'].Get()
        pwd = window['-LOGINPWD-'].Get()
        print('login details', uid, pwd)
        #dbConn = DBManager.DBManager.getDBConnection()
        #db_pos_cur = dbConn.cursor()
        #db_pos_cur.execute("SELECT * FROM tabUser WHERE USER_ID = '" + uid + "' AND PASSWORD='" + pwd + "'")
        #db_item_row = db_pos_cur.fetchone()
        db_item_row = dbOperation.verifyUser(uid,pwd)
        if db_item_row is not None:
            print('Login successfull...')
            window.hide()
            navigation()
        else:
            print('Login Failed.....')
            window['ErrMsg'].update('Invalid Credential')

