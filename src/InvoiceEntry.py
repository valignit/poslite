import re

import PySimpleGUI as sg
import sys
import mariadb
import platform
from datetime import date
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from DBOperations import DBOperations


db_pos_host = "localhost"
db_pos_port = 3306
db_pos_name = "alignpos"
db_pos_user = "alignpos"
db_pos_passwd = "valignit@2021"

column_heading = ['Barcode', 'Item Name', 'Unit', 'Qty', 'MRP', 'Disc.', 'Price', 'Tax', 'Net']
reader = "100000 ItemName Kg 100 26 0 26 0 2600", "100001 ItemName Kg 100 50 0 50 0 5000", "100002 ItemName Kg 100 20 0 20 0 2600", \
         "100000 ItemName Kg 100 26 0 26 0 2600", "100001 ItemName Kg 100 50 0 50 0 5000", "100002 ItemName Kg 100 20 0 20 0 2600"
#data1= ['100000 ItemName Kg 100 26 0 26 0 2600', '100001 ItemName Kg 100 50 0 50 0 5000', '100002 ItemName Kg 100 20 0 20 0 2600', '100000 ItemName Kg 100 26 0 26 0 2600', '100001 ItemName Kg 100 50 0 50 0 5000', '100002 ItemName Kg 100 20 0 20 0 2600']
reader = ""

data1 = list(reader)
print('data1=',data1)
data = list(reader)
#data = [['1','2','3','4','5','6','7','8','9']]
#data = [['8901314010322', 'Colgate strong teeth 150g', 'Nos', Decimal('70.000000'), Decimal('12.000000'), Decimal('12.000000'), Decimal('12.000000'), Decimal('12.000000')]]
itemData = ['8901314010322', '8906083130714', '8901030672446', '8902102162285', '8906033740758']

dbOperation = DBOperations(db_pos_host,db_pos_port,db_pos_name,db_pos_user,db_pos_passwd)
itemNames = dbOperation.fetchItemName()

def loadItemName():
    #itemData = [['8901314010322'], ['8906083130714'], ['8901030672446'], ['8902102162285'], ['8906033740758']]
    itemNames = dbOperation.fetchItemName()
    print("item data = ", itemNames)


def predict_text(searchItem, listItem):
    print('recied= ' ,searchItem, listItem)
    pattern = re.compile('.*' + searchItem + '.*')
    return [w for w in listItem if re.match(pattern, w)]

    #matches = []
    #matches = [match for match in listItem if searchItem in match]
    #return matches


def login_window():
    buttonLayout = [[sg.Button('Ok', pad=((0,0),(20,0)),key='-LoginOk-'), sg.Button('Cancel',pad=((0,0),(20,0)),key='-LoginCancel-')]]
    layout = [
              [sg.Text(' ',key='ErrMsg',size=(100,1)) ],
              [sg.Text('User Name:',pad=((0,0),(30,0)),size=(10,1)),sg.In(key='-LOGINUSER-', pad=((0,0),(30,0)) ,size=(100, 1))],
              [sg.Text('Password:',pad=((0,0),(10,0)),size=(10,1)),sg.In(key='-LOGINPWD-', password_char='*' , pad=((0,0),(10,0)), size=(100, 1))],
              [sg.Column(buttonLayout,vertical_alignment='center', justification='center') ]
              ]

    loginWindow = sg.Window('Login Window', keep_on_top=True, size=(300, 200), return_keyboard_events=True).Layout(layout)

    while True:             # Event Loop
        event, values = loginWindow.Read()
        if event is None or event == sg.WIN_CLOSED or event == '-LoginCancel-':
            loginWindow.Close()
            window.Close()
            break
        if event == '-LoginOk-':
            uid = loginWindow['-LOGINUSER-'].Get()
            pwd = loginWindow['-LOGINPWD-'].Get()
            print('login details',uid,pwd)
            if uid == 'admin' and pwd == '1234':
                print('Login successfull...')
                loginWindow.close()
            else:
                loginWindow['ErrMsg'].update('Invalid Credential')

def open_window():
    # print(predict_text('1', ['123']))
    choices = ['item-' + str(i) for i in range(30)]
    print("choices=", choices)
    # print(predict_text('1', values))
    # print(values)
    global itemNames
    layout = [  [sg.Text('Search Item:')],
                [sg.In(key='_INPUT_', size=(100,1))],
                [sg.Listbox(itemNames,  size=(100,10), key='_COMBO_', change_submits=True)],
                [sg.Button('Exit')]
             ]

    window1 = sg.Window('Window Title', keep_on_top=True ,size=(400,300),return_keyboard_events=True).Layout(layout)

    list_elem = window1.Element('_COMBO_')

    sel_item = 0
    while True:             # Event Loop
        event, values = window1.Read()
        if event is None or event == 'Exit':
            #window.FindElement('-BARCODE-NB-')
            window1.Close()
            break

        in_val = values['_INPUT_']
        if len(in_val) >=2:
            prediction_list = predict_text(str(in_val), itemNames)
            list_elem.Update(values=prediction_list)
            if prediction_list:
                print('list fired',prediction_list[0])
               # window.Element('_OUTPUT_').Update(prediction_list[0])
                #global window
               # values['-BARCODE-NB-'] =  prediction_list[0]
                justName = str(prediction_list[0]).split('~')
                window.FindElement('-ITEMNAME-').Update(justName[0])
                window.FindElement('-BARCODE-NB-').Update(justName[1])
                list_elem.Widget.itemconfigure(0,bg='green',fg='white')
        else:
            list_elem.Update(values=itemNames)
        if event == '_COMBO_':
            #sg.Popup('Chose', values['_COMBO_'])
            print('Chose2', values['_COMBO_'])
            #window.FindElement('-ITEMNAME-').Update(values['_COMBO_'])
            justName = str(values['_COMBO_']).split('~')
            window.FindElement('-ITEMNAME-').Update(justName[0])
            window.FindElement('-BARCODE-NB-').Update(justName[1])



"""
def open_window():

    layout = [[sg.Text("New Window", key="new")]]
    window = sg.Window("Second Window", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()
"""

def searchItemData(event):
    if len(window['Item-Name'].get()) >= 2:
        global itemData
        matches = []
        print('search item data',window['Item-Name'].get())
        searchItem =window['Item-Name'].get()
        window.Element('Item-Name').update(values=matches)
        matches = [match for match in itemData if searchItem in match]
        print("matches", matches)
        window.Element('Item-Name').update(values=matches)
        #window['Item-Name'].Widget.set(searchItem)
        window['Item-Name'].Widget.current(0)
        #window['Item-Name'].values[0]='test'

def exitPos():
    print('Exit Pos')

def deleteItem():
    print('Delete Item')

def verifyIn():
    print('focus in')

def verifyOut(event):
    barcode = window['-BARCODE-NB-'].get()
    if len(barcode) > 9:
        print(f'focuse out=',window['-BARCODE-NB-'].get())
        global data
        if any(barcode in data_list for data_list in data):
            return
        #if barcode in data:
         #   return

        itemdata = dbOperation.fetchItemData(barcode)
        print("data=",len(data))
        if len(data) > 0:
            data += itemdata
        else:
            data = itemdata
        print('item data =', data)
        #data = [['1','2','3','4','5','6','7','8','9']]
        #data = [['8901314010322', 'Colgate strong teeth 150g', 'Nos', '70.000000', '12.000000','12.000000', '12.000000', '12.000000']]
        window['-TABLE-'].update(values=data)

def tableFocus():
    # Re-Grab table focus using ttk
    if(len(data) > 0):
        window['-TABLE-'].Widget.config(takefocus=1)
        table_row = window['-TABLE-'].Widget.get_children()[0]
        window['-TABLE-'].Widget.selection_set(table_row)  # move selection
        window['-TABLE-'].Widget.focus(table_row)  # move focus
        window['-TABLE-'].Widget.see(table_row)  # scroll to show i

def disableFocus():
    window['-USERID-'].Widget.config(takefocus=0)
    window['-TERMINAL-'].Widget.config(takefocus=0)
    window['-DATE-'].Widget.config(takefocus=0)

    window['-INVOICE-NB-'].Widget.config(takefocus=0)
    window['-MOBILE-NB-'].Widget.config(takefocus=0)
    window['-CUSTOMER-'].Widget.config(takefocus=0)

    window['F1'].Widget.config(takefocus=0)
    #window['F2'].Widget.config(takefocus=0)
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

    window['-Lines-items-'].Widget.config(takefocus=0)
    window['-Total-qty-'].Widget.config(takefocus=0)
    window['-mrp-'].Widget.config(takefocus=0)
    window['-Discounts-'].Widget.config(takefocus=0)
    window['-Price-'].Widget.config(takefocus=0)
    window['-tax-'].Widget.config(takefocus=0)
    window['-Net-Amt-'].Widget.config(takefocus=0)
    window['-paid-amt-'].Widget.config(takefocus=0)

    window['T1'].Widget.config(takefocus=0)
    window['T2'].Widget.config(takefocus=0)
    window['T3'].Widget.config(takefocus=0)
    window['T4'].Widget.config(takefocus=0)
    window['T5'].Widget.config(takefocus=0)
    window['T6'].Widget.config(takefocus=0)
    window['T7'].Widget.config(takefocus=0)
    window['T8'].Widget.config(takefocus=0)
    window['T9'].Widget.config(takefocus=0)
    window['TUP'].Widget.config(takefocus=0)
    window['TDN'].Widget.config(takefocus=0)
    window['TRT'].Widget.config(takefocus=0)
    window['TLT'].Widget.config(takefocus=0)

    window['TZR'].Widget.config(takefocus=0)
    window['TEN'].Widget.config(takefocus=0)
    window['TPU'].Widget.config(takefocus=0)

    window['TPD'].Widget.config(takefocus=0)
    window['TDT'].Widget.config(takefocus=0)
    window['TCL'].Widget.config(takefocus=0)

today = date.today()

# sg.ChangeLookAndFeel('GreenTan')
sg.theme('SystemDefault')
# sg.set_options(element_padding=(0, 0))
theme_name_list = sg.theme_list()
# print(theme_name_list)
win_w, win_h = sg.Window.get_screen_size()
win_w = win_w - 100
win_h = win_h - 100

col1= int(win_w) - int((win_w*30/100))
col2= int((win_w*30/100))
print(win_w,win_h,col1,col2)
print(sys.version)
print(sys.version_info.major)
print(platform.python_version())
print(type(platform.python_version()))

element_w = 10
element_h = 2
if win_w > 1250:
    element_w=15
    element_h=2

col1_size=(col1, 50)
col1_w=col1
tab_h=350
col2_w=col2

btn_pad_pg: dict = {'size': (4, 2), 'font': ('Helvetica 11 bold'), 'button_color':("sky blue")}
btn_pad: dict = {'size': (4, 2), 'font': ('Helvetica 11 bold'), 'button_color':("sky blue")}
input_fld: dict = {'readonly':'True', 'disabled_readonly_text_color':'gray','disabled_readonly_background_color':'gray89', 'font':("Helvetica", 12),'size':(15, 1)}
input_font: dict = {'font': ('Helvetica 12')}
btm_btn: dict = {'size':(10, 2), 'font':'Helvetica 11 bold'}
sum_info: dict ={'readonly':True, 'disabled_readonly_text_color':'gray','disabled_readonly_background_color':'gray89', 'font':("Helvetica", 11),'size':(12, 1)}
sum_info_font: dict = {'font':('Helvetica 11'), 'justification':'right', 'size':(10, 1)}
inv_label_font: dict = {'size':(15, 1), 'font':('Helvetica 20')}
btn_ent : dict ={'size':(element_w,element_h), 'font':'Helvetica 11 bold', 'button_color':'cornflower blue'}

wvar = tk.StringVar

col_1_Layout = [
    [
        sg.Column(
            [
                [
                    sg.Text('Invoice Entry', **inv_label_font),
                    sg.Text('User:', **input_font),
                    sg.Input(key='-USERID-', **input_fld),
                    sg.Text('Terminal:', **input_font),
                    sg.Input(key='-TERMINAL-', **input_fld),
                    sg.Text('Date:', **input_font),
                    sg.Input(key='-DATE-', **input_fld,default_text=today.strftime("%m/%d/%y"))
                ]
            ], size=col1_size, vertical_alignment='top')
    ],
    [
        sg.Column(
            [
                [
                    sg.Text('Invoice No', **input_font),
                    sg.Input(key='-INVOICE-NB-',**input_fld),
                    sg.Text('Mobile No.:', **input_font),
                    sg.Input(key='-MOBILE-NB-', **input_fld),
                    sg.Text('Customer:', **input_font),
                    sg.Input(key='-CUSTOMER-', **input_fld),
                    sg.Text('UNPAID', font=("Helvetica", 15))
                ]
            ], size=col1_size, vertical_alignment='top')
    ],
    [
        sg.Column(
            [
                [
                    sg.Text('Barcode:', size=(8, 1), font=("Helvetica", 12)),
                    sg.Input(key='-BARCODE-NB-', background_color='White', font=("Helvetica", 12), size=(15, 1), focus=True,enable_events=True),
                    sg.Text('Item Name:', size=(12, 1), font=("Helvetica", 12)),
                    sg.InputCombo(('8901314010322'), background_color='White' ,auto_size_text=True, font=("Helvetica", 12),
                                  size=(20, 20), key='Item-Name' ),
                    sg.Input(key='-ITEMNAME-', background_color='White', font=("Helvetica", 12), size=(15, 1)),
                    sg.Button('Search Item', border_width=2,**btm_btn , key='-SEARCH-ITME-'),
                ]
            ], size=col1_size, vertical_alignment='top')
    ],
    [
        sg.Column(
            [
                [
                    sg.Table(values=data,
                             key='-TABLE-',
                             headings=column_heading,
                             font=(("Helvetica", 11)),
                             # max_col_width=500,
                             auto_size_columns=False,
                             justification='right',
                             row_height=25,
                             alternating_row_color='lightsteelBlue1',
                             num_rows=15,
                             col_widths=[12, 10, 10, 10, 10, 10, 12, 10, 12],
                             enable_events=True,
                             bind_return_key=True
                             )
                ]
            ], size=(col1_w, tab_h), vertical_alignment='top'
        )
    ],
    [
        sg.Column(
            [
                [
                    sg.Button('F1\nHelp', border_width=2,**btm_btn , key='F1'),
                    sg.Button('F2\nDel Item', border_width=2, **btm_btn, key='F2'),
                    sg.Button('F3\nLookup', border_width=2, **btm_btn, key='F3'),
                    sg.Button('F4\nChange Qty', border_width=2, **btm_btn, key='F4'),
                    sg.Button('F5\nChange Price', border_width=2, **btm_btn, key='F5'),
                    sg.Button('F6\nGet Weight', border_width=2, **btm_btn, key='F6')
                ],
                [
                    sg.Button('F7\nNew Invoice',border_width=2, **btm_btn, key='F7'),
                    sg.Button('F8\nDel Invoice', border_width=2 ,**btm_btn, key='F8'),
                    sg.Button('F9\nLookup Cust', border_width=2,**btm_btn, key='F9'),
                    sg.Button('F10\nList Invoices', border_width=2,**btm_btn, key='F10'),
                    sg.Button('F11\nPrint Invoices', border_width=2,**btm_btn, key='F11'),
                    sg.Button('F12\nPayment', border_width=2,**btm_btn, key='F12'),
                    sg.Button('Esc-Exit', border_width=2,**btm_btn, key='ESC')

                ]
            ], size=(col1_w, 150), vertical_alignment='top')
    ]
]

col_2_Layout = [
    [
        sg.Column(
            [
                [
                    sg.Image(filename='company-logo.GIF')
                ]
            ], size=(col2_w, 90), vertical_alignment='top')
    ],
    [
        sg.Column(
            [
                [
                    sg.Text('Lines Items:', **sum_info_font),
                    sg.Input(key='-Lines-items-',**sum_info)
                ],
                [
                    sg.Text('Total Qty:', **sum_info_font),
                    sg.Input(key='-Total-qty-', **sum_info)
                ],
                [
                    sg.Text('MRP:', **sum_info_font),
                    sg.Input(key='-mrp-', **sum_info),
                ],
                [
                    sg.Text('Discounts:', **sum_info_font),
                    sg.Input(key='-Discounts-', **sum_info),
                ],
                [
                    sg.Text('Price:', **sum_info_font),
                    sg.Input(key='-Price-', **sum_info),
                ],
                [
                    sg.Text('Tax:', **sum_info_font),
                    sg.Input(key='-tax-',  **sum_info)
                ],
                [
                    sg.Text('Net Amt:', **sum_info_font),
                    sg.Input(key='-Net-Amt-', **sum_info),
                ],
                [
                    sg.Text('Paid Amt:', **sum_info_font),
                    sg.Input(key='-paid-amt-', **sum_info)
                ]

            ], size=(col2_w, 220), vertical_alignment='top')
    ],
    [
        sg.Column(
            [
                [
                    sg.Button('\u2191', **btn_pad , key='TUP'),
                    sg.Button('7', **btn_pad , key='T7'),
                    sg.Button('8', **btn_pad , key='T8'),
                    sg.Button('9', **btn_pad , key='T9'),

                ],
                [
                    sg.Button('\u2193', **btn_pad ,key='TDN'),
                    sg.Button('4', **btn_pad ,key='T4' ),
                    sg.Button('5', **btn_pad ,key='T5' ),
                    sg.Button('6', **btn_pad , key='T6' ),
                ],
                [
                    sg.Button('\u2192', **btn_pad, key='TRT'),
                    sg.Button('1', **btn_pad, key='T1'),
                    sg.Button('2', **btn_pad, key='T2'),
                    sg.Button('3', **btn_pad, key='T3'),

                ],
                [
                    sg.Button('\u2190', **btn_pad, key='TLT'),
                    sg.Button('0', **btn_pad, key='TZR'),
                    sg.Button('Enter', **btn_ent, key='TEN'),
                ],
                [
                    sg.Button('Up', **btn_pad_pg, key='TPU'),
                    sg.Button('Dn', **btn_pad_pg, key='TPD'),
                    sg.Button('.', **btn_pad, key='TDT'),
                    sg.Button('C', **btn_pad, key='TCL')
                ]
            ], size=(col2_w, 290), vertical_alignment='top')
    ],
    [
        sg.Column(
            [
            ], size=(col2_w, 63), vertical_alignment='top')
    ]
]

mainLayout = [
    [
        sg.Column(col_1_Layout, background_color='lightblue', vertical_alignment='top'),

        sg.Column(col_2_Layout, background_color='lightblue', vertical_alignment='top'),
    ]
]
window = sg.Window('POS', mainLayout, location=(0, 0), size=(win_w, win_h), use_default_focus=False, finalize=True, resizable=True)

#window['-BARCODE-NB-'].bind('<FocusOut>', verifyOut)
window['-BARCODE-NB-'].Widget.bind('<FocusOut>', verifyOut)
window['Item-Name'].Widget.bind('<Enter>', searchItemData)
#window['F2'].Widget.bind('<F2>', deleteItem)
#window['F2'].Widget.bind('<F2>', window['F2'].deleteItem)
window.bind('<F1>', '')
window.bind('<F2>', deleteItem())
window.bind('<F3>', '')
window.bind('<F4>', '')
window.bind('<F5>', '')
window.bind('<F6>', '')
window.bind('<F7>', '')
window.bind('<F8>', '')
window.bind('<F9>', '')
window.bind('<F10>', '')
window.bind('<F11>', '')
window.bind('<F12>', '')
window.bind('<Escape>', exitPos())

disableFocus()
tableFocus()
loadItemName()
selected_row = None

login_window()

while True:
    event, values = window.read()
    #print(event, values)
    if event == '<F2>':
        print("deleting selected items...")
        if selected_row is not None:
            data.pop(selected_row)
            selected_row = None
            window.Element('-TABLE-').update(values=data)
    if event == sg.WIN_CLOSED:
        print('close window')
        if sg.popup_yes_no('Do you want to Exit?',title='Confirmation', keep_on_top=True) == 'Yes':
            break

    if event == '<Escape>':
        if sg.popup_yes_no('Do you want to Exit?',title='Confirmation', keep_on_top=True) == 'Yes':
            break
    if event == '-TABLE-':
        selected_row = values['-TABLE-'][0]
        print("select row ", selected_row)
    if event == "-SEARCH-ITME-":
        print('search item')
        open_window()
    if event == "ESC":
        if sg.popup_yes_no('Do you want to Exit?', title='Confirmation', keep_on_top=True) == 'Yes':
            break