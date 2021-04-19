import PySimpleGUI as sg
import sys
import platform
from datetime import date

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

bw: dict = {'size': (4, 2), 'font': ('Helvetica 11 bold'), 'button_color':("sky blue")}
it: dict = {'readonly':'True', 'disabled_readonly_text_color':'gray','disabled_readonly_background_color':'gray89', 'font':("Helvetica", 12),'size':(15, 1)}
in_font: dict = {'font': ('Helvetica 12')}
btm_btn: dict = {'size':(10, 2), 'font':'Helvetica 11 bold'}
sum_info: dict ={'readonly':True, 'disabled_readonly_text_color':'gray','disabled_readonly_background_color':'gray89', 'font':("Helvetica", 11),'size':(12, 1)}
sum_info_font: dict = {'font':('Helvetica 11'), 'justification':'right', 'size':(10, 1)}
inv_label_font: dict = {'size':(15, 1), 'font':('Helvetica 20')}


btn_ent : dict ={'size':(element_w,element_h), 'font':'Helvetica 11 bold', 'button_color':'cornflower blue'}
column_heading = ['Barcode', 'Item Name', 'Unit', 'Qty', 'MRP', 'Disc.', 'Price', 'Tax', 'Net']
reader = "100000 ItemName Kg 100 26 0 26 0 2600", "100001 ItemName Kg 100 50 0 50 0 5000", "100002 ItemName Kg 100 20 0 20 0 2600", \
         "100000 ItemName Kg 100 26 0 26 0 2600", "100001 ItemName Kg 100 50 0 50 0 5000", "100002 ItemName Kg 100 20 0 20 0 2600"
data1 = list(reader)

col_1_Layout = [
    [
        sg.Column(
            [
                [
                    sg.Text('Invoice Entry', **inv_label_font),
                    sg.Text('User:', **in_font),
                    sg.Input(key='-USERID-', **it,default_text='admin'),
                    sg.Text('Terminal:', **in_font),
                    sg.Input(key='-TERMINAL-', **it,default_text='Terminal100'),
                    sg.Text('Date:', **in_font),
                    sg.Input(key='-DATE-', **it,default_text=today.strftime("%m/%d/%y"))
                ]
            ], size=col1_size, vertical_alignment='top')
    ],
    [
        sg.Column(
            [
                [
                    sg.Text('Invoice No', **in_font),
                    sg.Input(key='-INVOICE-NB-',**it),
                    sg.Text('Mobile No.:', **in_font),
                    sg.Input(key='-MOBILE-NB-', **it),
                    sg.Text('Customer:', **in_font),
                    sg.Input(key='-CUSTOMER-', **it),
                    sg.Text('UNPAID', font=("Helvetica", 15))
                ]
            ], size=col1_size, vertical_alignment='top')
    ],
    [
        sg.Column(
            [
                [
                    sg.Text('Barcode:', size=(8, 1), font=("Helvetica", 12)),
                    sg.Input(key='-BARCODE-NB-', background_color='White', font=("Helvetica", 12), size=(15, 1), focus=True),
                    sg.Text('Item Name:', size=(12, 1), font=("Helvetica", 12)),
                    sg.InputCombo(('Item Name', 'Item Name'), background_color='White', font=("Helvetica", 12),
                                  size=(40, 1))
                ]
            ], size=col1_size, vertical_alignment='top')
    ],
    [
        sg.Column(
            [
                [
                    sg.Table(values=data1,
                             headings=column_heading,
                             font=(("Helvetica", 11)),
                             # max_col_width=500,
                             auto_size_columns=False,
                             justification='right',
                             row_height=25,
                             alternating_row_color='lightsteelBlue1',
                             num_rows=15,
                             col_widths=[12, 10, 10, 10, 10, 10, 12, 10, 12]
                             )
                ]
            ], size=(col1_w, tab_h), vertical_alignment='top')
    ],
    [
        sg.Column(
            [
                [
                    sg.SimpleButton('F1\nHelp', border_width=2,**btm_btn , key='F1'),
                    sg.SimpleButton('F2\nDel Item', border_width=2, **btm_btn, key='F2'),
                    sg.SimpleButton('F3\nLookup', border_width=2, **btm_btn, key='F3'),
                    sg.SimpleButton('F4\nChange Qty', border_width=2, **btm_btn, key='F4'),
                    sg.SimpleButton('F5\nChange Price', border_width=2, **btm_btn, key='F1'),
                    sg.SimpleButton('F6\nGet Weight', border_width=2, **btm_btn, key='F2')
                ],
                [
                    sg.SimpleButton('F7\nGet Weight',border_width=2, **btm_btn, key='F7'),
                    sg.SimpleButton('F8\nNew Invoice', border_width=2 ,**btm_btn, key='F8'),
                    sg.SimpleButton('F9\nDel Invoice', border_width=2,**btm_btn, key='F9'),
                    sg.SimpleButton('F10\nLookup Cust', border_width=2,**btm_btn, key='F10'),
                    sg.SimpleButton('F11\nList Invoices', border_width=2,**btm_btn, key='F11'),
                    sg.SimpleButton('F12\nPrint Invoices', border_width=2,**btm_btn, key='F12'),
                    sg.SimpleButton('Esc-Exit', border_width=2,**btm_btn, key='F7')

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
                    sg.Text('Lines Items:', **sum_info_font ),
                    sg.Input(key='-Lines-items-',**sum_info,default_text='6')
                ],
                [
                    sg.Text('Total Qty:', **sum_info_font),
                    sg.Input(key='-Total-qty-', **sum_info ,default_text='600')
                ],
                [
                    sg.Text('MRP:', **sum_info_font),
                    sg.Input(key='-mrp-', **sum_info ,default_text='2600'),
                ],
                [
                    sg.Text('Discounts:', **sum_info_font),
                    sg.Input(key='-Discounts-', **sum_info ,default_text='0.0'),
                ],
                [
                    sg.Text('Price:', **sum_info_font),
                    sg.Input(key='-Price-', **sum_info ,default_text='2600.0'),
                ],
                [
                    sg.Text('Tax:', **sum_info_font),
                    sg.Input(key='-tax-',  **sum_info ,default_text='0.0')
                ],
                [
                    sg.Text('Net Amt:', **sum_info_font),
                    sg.Input(key='-Net-Amt-', **sum_info ,default_text='2600'),
                ],
                [
                    sg.Text('Paid Amt:', **sum_info_font),
                    sg.Input(key='-paid-amt-', **sum_info ,default_text='2600')
                ]

            ], size=(col2_w, 220), vertical_alignment='top')
    ],
    [
        sg.Column(
            [
                [
                    sg.SimpleButton('\u2191', **bw , key='T1'),
                    sg.SimpleButton('7', **bw , key='T2'),
                    sg.SimpleButton('8', **bw , key='T3'),
                    sg.SimpleButton('9', **bw , key='T3'),

                ],
                [
                    sg.SimpleButton('\u2193', **bw ,key='T1'),
                    sg.SimpleButton('4', **bw ,key='T2' ),
                    sg.SimpleButton('5', **bw ,key='T3' ),
                    sg.SimpleButton('6', **bw , key='T3' ),
                ],
                [
                    sg.SimpleButton('\u2192', **bw, key='T1'),
                    sg.SimpleButton('1', **bw, key='T2'),
                    sg.SimpleButton('2', **bw, key='T3'),
                    sg.SimpleButton('3', **bw, key='T3'),

                ],
                [
                    sg.SimpleButton('\u2190', **bw, key='T1'),
                    sg.SimpleButton('.', **bw, key='T2'),
                    sg.SimpleButton('Enter', **btn_ent, key='TE'),
                ],
                [
                    sg.SimpleButton('+', **bw, key='T1'),
                    sg.SimpleButton('-', **bw, key='T2'),
                    sg.SimpleButton('D', **bw, key='T3'),
                    sg.SimpleButton('C', **bw, key='T3'),

                ]
            ], size=(col2_w, 285), vertical_alignment='top')
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

window = sg.Window('POS', mainLayout, location=(0, 0), size=(win_w, win_h)
                   )

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
