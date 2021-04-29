import PySimpleGUI as sg
import sys
import mariadb
import platform
from datetime import date
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
#import src.DBOperations
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

def searchItemData(event):
    if len(window['Item-Name'].get()) > 2:
        global itemData
        matches = []
        print('search item data',window['Item-Name'].get())
        searchItem =window['Item-Name'].get()
        window.Element('Item-Name').update(values=matches)
        matches = [match for match in itemData if searchItem in match]
        print("matches", matches)
        window.Element('Item-Name').update(values=matches)

def loadItemName():
    itemData = [['8901314010322'], ['8906083130714'], ['8901030672446'], ['8902102162285'], ['8906033740758']]

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
                    sg.InputCombo(('8901314010322'), background_color='White', font=("Helvetica", 12),
                                  size=(40, 30), key='Item-Name' )
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
                    sg.SimpleButton('F1\nHelp', border_width=2,**btm_btn , key='F1'),
                    sg.SimpleButton('F2\nDel Item', border_width=2, **btm_btn, key='F2'),
                    sg.SimpleButton('F3\nLookup', border_width=2, **btm_btn, key='F3'),
                    sg.SimpleButton('F4\nChange Qty', border_width=2, **btm_btn, key='F4'),
                    sg.SimpleButton('F5\nChange Price', border_width=2, **btm_btn, key='F5'),
                    sg.SimpleButton('F6\nGet Weight', border_width=2, **btm_btn, key='F6')
                ],
                [
                    sg.SimpleButton('F7\nNew Invoice',border_width=2, **btm_btn, key='F7'),
                    sg.SimpleButton('F8\nDel Invoice', border_width=2 ,**btm_btn, key='F8'),
                    sg.SimpleButton('F9\nLookup Cust', border_width=2,**btm_btn, key='F9'),
                    sg.SimpleButton('F10\nList Invoices', border_width=2,**btm_btn, key='F10'),
                    sg.SimpleButton('F11\nPrint Invoices', border_width=2,**btm_btn, key='F11'),
                    sg.SimpleButton('F12\nPayment', border_width=2,**btm_btn, key='F12'),
                    sg.SimpleButton('Esc-Exit', border_width=2,**btm_btn, key='ESC')

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
                    sg.SimpleButton('\u2191', **btn_pad , key='TUP'),
                    sg.SimpleButton('7', **btn_pad , key='T7'),
                    sg.SimpleButton('8', **btn_pad , key='T8'),
                    sg.SimpleButton('9', **btn_pad , key='T9'),

                ],
                [
                    sg.SimpleButton('\u2193', **btn_pad ,key='TDN'),
                    sg.SimpleButton('4', **btn_pad ,key='T4' ),
                    sg.SimpleButton('5', **btn_pad ,key='T5' ),
                    sg.SimpleButton('6', **btn_pad , key='T6' ),
                ],
                [
                    sg.SimpleButton('\u2192', **btn_pad, key='TRT'),
                    sg.SimpleButton('1', **btn_pad, key='T1'),
                    sg.SimpleButton('2', **btn_pad, key='T2'),
                    sg.SimpleButton('3', **btn_pad, key='T3'),

                ],
                [
                    sg.SimpleButton('\u2190', **btn_pad, key='TLT'),
                    sg.SimpleButton('0', **btn_pad, key='TZR'),
                    sg.SimpleButton('Enter', **btn_ent, key='TEN'),
                ],
                [
                    sg.SimpleButton('Up', **btn_pad_pg, key='TPU'),
                    sg.SimpleButton('Dn', **btn_pad_pg, key='TPD'),
                    sg.SimpleButton('.', **btn_pad, key='TDT'),
                    sg.SimpleButton('C', **btn_pad, key='TCL')
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
window['Item-Name'].Widget.bind('<Key>', searchItemData)
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
        break
    if event == '<Escape>':
        if sg.popup_yes_no('Do you want to Exit?',title='Confirmation', keep_on_top=True) == 'Yes':
            break
    if event == '-TABLE-':
        selected_row = values['-TABLE-'][0]
        print("select row ", selected_row)