import PySimpleGUI as sg
import sys
import platform
from datetime import date

class InvoiceLayout:

    reader = ""
    data1 = list(reader)
    print('data1=', data1)
    data = list(reader)
    column_heading = ['Item code', 'Barcode', 'Item Name', 'Unit', 'Qty', 'Price', 'Amount', 'Tax Rate', 'Tax', 'Net']
    disabled_text_color = 'grey32'
    pad_button_color = 'SteelBlue3'
    list_items = []
    function_button_color = 'SteelBlue3'
    win_w, win_h = sg.Window.get_screen_size()
    #win_w = win_w - 100
    #win_h = win_h - 100

    col1 = int(win_w) - int((win_w * 30 / 100))
    col2 = int((win_w * 30 / 100))
    print(win_w, win_h, col1, col2)
    print(sys.version)
    print(sys.version_info.major)
    print(platform.python_version())
    print(type(platform.python_version()))

    today = date.today()

    element_w = 10
    element_h = 2
    if win_w > 1250:
        element_w = 15
        element_h = 2

    col1_size = (col1, 50)
    col1_w = col1
    tab_h = 350
    col2_w = col2

    btn_pad_pg: dict = {'size': (4, 2), 'font': ('Helvetica 11 bold'), 'button_color': ("sky blue")}
    btn_pad: dict = {'size': (4, 2), 'font': ('Helvetica 11 bold'), 'button_color': ("sky blue")}
    input_fld: dict = {'readonly': 'True', 'disabled_readonly_text_color': 'gray',
                       'disabled_readonly_background_color': 'gray89', 'font': ("Helvetica", 12), 'size': (15, 1)}
    input_font: dict = {'font': ('Helvetica 12')}
    btm_btn: dict = {'size': (10, 2), 'font': 'Helvetica 11 bold'}
    sum_info: dict = {'readonly': True, 'disabled_readonly_text_color': 'gray',
                      'disabled_readonly_background_color': 'gray89', 'font': ("Helvetica", 11), 'size': (12, 1)}
    sum_info_font: dict = {'font': ('Helvetica 11'), 'justification': 'right', 'size': (10, 1)}
    inv_label_font: dict = {'size': (15, 1), 'font': ('Helvetica 20')}
    btn_ent: dict = {'size': (element_w, element_h), 'font': 'Helvetica 11 bold', 'button_color': 'cornflower blue'}

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
                        sg.Input(key='-INVOICE_NO-',**input_fld),
                        sg.Text('Reference No:', **input_font),
                        sg.Input(key='-REFERENCE_NO-', **input_font),
                        sg.Text('Mobile No.:', **input_font),
                        sg.Input(key='-MOBILE_NO-', **input_fld),
                        sg.Text('Customer:', **input_font),
                        sg.Input(key='-CUSTOMER-', **input_fld),
                        sg.Text('UNPAID', font=("Helvetica", 15)),
                        sg.Button('PREV\n←', size=(8, 2), font='Calibri 12 bold', key='PREV',
                                  button_color=pad_button_color),
                        sg.Button('NEXT\n→', size=(8, 2), font='Calibri 12 bold', key='NEXT',
                                  button_color=pad_button_color)
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
                        sg.Text('Line Items:',  **sum_info_font),
                        sg.Input(key='-LINE-ITEMS-', **sum_info)
                    ],
                    [
                        sg.Text('Total Qty:',  **sum_info_font),
                        sg.Input(key='-TOTAL-QTY-',**sum_info)
                    ],
                    [
                        sg.Text('Total Price:',  **sum_info_font),
                        sg.Input(key='-TOTAL-PRICE-', **sum_info),
                    ],
                    [
                        sg.Text('Tax:',  **sum_info_font),
                        sg.Input(key='-TOTAL-TAX-',**sum_info),
                    ],
                    [
                        sg.Text('Net Price:',  **sum_info_font),
                        sg.Input(key='-NET-PRICE-', **sum_info),
                    ],
                    [
                        sg.Text('Discount:',  **sum_info_font),
                        sg.Input(key='-DISCOUNT-', **sum_info),
                    ],
                    [
                        sg.Text('Invoice Amt:',  **sum_info_font),
                        sg.Input(key='-INVOICE-AMT-', **sum_info),
                    ],
                    [
                        sg.Text('Paid Amt:',  **sum_info_font),
                        sg.Input(key='-PAID-AMT-', **sum_info)
                    ]
                ], size=(col2_w, 220), vertical_alignment='top')
        ],
        [
            sg.Column(
                [
                    [
                        sg.Button('\u2191', **btn_pad , key='UP'),
                        sg.Button('7', **btn_pad , key='T7'),
                        sg.Button('8', **btn_pad , key='T8'),
                        sg.Button('9', **btn_pad , key='T9'),

                    ],
                    [
                        sg.Button('\u2193', **btn_pad ,key='DOWN'),
                        sg.Button('4', **btn_pad ,key='T4' ),
                        sg.Button('5', **btn_pad ,key='T5' ),
                        sg.Button('6', **btn_pad , key='T6' ),
                    ],
                    [
                        sg.Button('\u2192', **btn_pad, key='RIGHT'),
                        sg.Button('1', **btn_pad, key='T1'),
                        sg.Button('2', **btn_pad, key='T2'),
                        sg.Button('3', **btn_pad, key='T3'),

                    ],
                    [
                        sg.Button('\u2190', **btn_pad, key='LEFT'),
                        sg.Button('0', **btn_pad, key='T0'),
                        sg.Button('Enter', **btn_ent, key='ENTER'),
                    ],
                    [
                        sg.Button('<<', **btn_pad_pg, key='BACK-SPACE'),
                        sg.Button('Dn', **btn_pad_pg, key='TPD'),
                        sg.Button('.', **btn_pad, key='FULL-STOP'),
                        sg.Button('TAB', **btn_pad, key='TAB')
                    ]
                ], size=(col2_w, 290), vertical_alignment='top')
        ],
        [
            sg.Column(
                [
                ], size=(col2_w, 63), vertical_alignment='top')
        ]
    ]

    layout_main = [
        [
            sg.Column(col_1_Layout, background_color='lightblue', vertical_alignment='top'),

            sg.Column(col_2_Layout, background_color='lightblue', vertical_alignment='top'),
        ]
    ]


""""
    layout_column_1 = [
        [
            sg.Column(
                [
                    [
                        sg.Text('Invoice Entry', size=(15, 1), font=("Helvetica", 20)),
                        sg.Text('User:', font=("Helvetica", 12)),
                        sg.Input(key='-USERID-', readonly=True, disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='admin',
                                 font=("Helvetica", 12), size=(15, 1)),
                        sg.Text('Terminal:', font=("Helvetica", 12)),
                        sg.Input(key='-TERMINAL-', readonly=True, disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='Terminal100',
                                 font=("Helvetica", 12), size=(15, 1)),
                        sg.Text('Date:', font=("Helvetica", 12)),
                        sg.Input(key='-DATE-', readonly=True, disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='16-apr-2021',
                                 font=("Helvetica", 12), size=(15, 1)),
                    ]
                ], size=col1_size, vertical_alignment='top', pad=None)
        ],
        [
            sg.Column(
                [
                    [
                        sg.Text('Invoice No:', size=(8, 1), font=("Helvetica", 12)),
                        sg.Input(key='-INVOICE_NO-', readonly=True, disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='SINV-0010',
                                 font=("Helvetica", 12), size=(15, 1)),
                        sg.Text('Reference No:', size=(8, 1), font=("Helvetica", 12)),
                        sg.Input(key='-REFERENCE_NO-', readonly=True, disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='0022',
                                 font=("Helvetica", 12), size=(15, 1)),
                        sg.Text('Mobile No:', size=(8, 1), font=("Helvetica", 12)),
                        sg.Input(key='-MOBILE_NO-', readonly=True, disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='0000000000',
                                 font=("Helvetica", 12), size=(15, 1)),
                        sg.Text('UNPAID', font=("Helvetica", 15)),
                        sg.Button('PREV\n←', size=(8, 2), font='Calibri 12 bold', key='PREV',
                                  button_color=pad_button_color),
                        sg.Button('NEXT\n→', size=(8, 2), font='Calibri 12 bold', key='NEXT',
                                  button_color=pad_button_color),
                    ]
                ], size=col1_size, vertical_alignment='top', pad=None)
        ],
        [
            sg.Column(
                [
                    [
                        sg.Text('Barcode:', size=(8, 1), font=("Helvetica", 12)),
                        sg.Input(key='-BARCODE-NB-', background_color='White', font=("Helvetica", 12), size=(15, 1),
                                 enable_events=True),
                        sg.Text('Item Name:', size=(8, 1), font=("Helvetica", 12)),
                        sg.Input(key='-ITEM_NAME-', background_color='White', font=("Helvetica", 12), size=(25, 1),
                                 enable_events=True),
                    ]
                ], size=col1_size, vertical_alignment='top', pad=None)
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
                                 col_widths=[12, 10, 10, 10, 10, 10, 12, 10, 12]
                                 )
                    ]
                ], size=(col1_w, tab_h), vertical_alignment='top', pad=None)
        ],
        [
            sg.Column(
                [
                    [
                        sg.Button('Help\nF1', size=(13, 2), font='Helvetica 11 bold', key='F1',
                                  button_color=function_button_color),
                        sg.Button('F2\nDel Item', size=(13, 2), font='Helvetica 11 bold', key='F2',
                                  button_color=function_button_color),
                        sg.Button('F3\nFind Item', size=(13, 2), font='Helvetica 11 bold', key='F3',
                                  button_color=function_button_color),
                        sg.Button('F4\nChange Quantity', size=(13, 2), font='Helvetica 11 bold', key='F4',
                                  button_color=function_button_color),
                        sg.Button('F5\nChange Price', size=(13, 2), font='Helvetica 11 bold', key='F5',
                                  button_color=function_button_color),
                        sg.Button('F6\nGet Weight', size=(13, 2), font='Helvetica 11 bold', key='F6',
                                  button_color=function_button_color)
                    ],
                    [
                        sg.Button('F7\nNew Invoice', size=(13, 2), font='Helvetica 11 bold', key='F7',
                                  button_color=function_button_color),
                        sg.Button('F8\nDelete Invoice', size=(13, 2), font='Helvetica 11 bold', key='F8',
                                  button_color=function_button_color),
                        sg.Button('F9\nFind Customer', size=(13, 2), font='Helvetica 11 bold', key='F9',
                                  button_color=function_button_color),
                        sg.Button('F10\nList Invoices', size=(13, 2), font='Helvetica 11 bold', key='F10',
                                  button_color=function_button_color),
                        sg.Button('F11\nPrint Invoice', size=(13, 2), font='Helvetica 11 bold', key='F11',
                                  button_color=function_button_color),
                        sg.Button('F12\nPayment', size=(13, 2), font='Helvetica 11 bold', key='F12',
                                  button_color=function_button_color),
                        sg.Button('Esc\nExit', size=(13, 2), font='Helvetica 11 bold', key='ESC',
                                  button_color=function_button_color)
                    ]
                ], size=(col1_w, 150), background_color='gray80', vertical_alignment='top', pad=None)
        ]
    ]

    layout_column_2 = [
        [
            sg.Column(
                [
                    [
                        sg.Image(filename='company-logo.GIF')
                    ]
                ], size=(col2_w, 90), vertical_alignment='top', pad=None)
        ],
        [
            sg.Column(
                [
                    [
                        sg.Text('Line Items:', font=("Helvetica", 11), justification="right", size=(10, 1)),
                        sg.Input(key='-LINE-ITEMS-', readonly=True, justification="right",
                                 disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='0', font=("Helvetica", 11),
                                 size=(12, 1))
                    ],
                    [
                        sg.Text('Total Qty:', font=("Helvetica", 11), justification="right", size=(10, 1)),
                        sg.Input(key='-TOTAL-QTY-', readonly=True, justification="right",
                                 disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='0.00',
                                 font=("Helvetica", 11), size=(12, 1))
                    ],
                    [
                        sg.Text('Total Price:', font=("Helvetica", 11), justification="right", size=(10, 1)),
                        sg.Input(key='-TOTAL-PRICE-', readonly=True, justification="right",
                                 disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='0.00',
                                 font=("Helvetica", 11), size=(12, 1)),
                    ],
                    [
                        sg.Text('Tax:', font=("Helvetica", 11), justification="right", size=(10, 1)),
                        sg.Input(key='-TOTAL-TAX-', readonly=True, justification="right",
                                 disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='0.00',
                                 font=("Helvetica", 11), size=(12, 1)),
                    ],
                    [
                        sg.Text('Net Price:', font=("Helvetica", 11), justification="right", size=(10, 1)),
                        sg.Input(key='-NET-PRICE-', readonly=True, justification="right",
                                 disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='0.00',
                                 font=("Helvetica", 11), size=(12, 1)),
                    ],
                    [
                        sg.Text('Discount:', font=("Helvetica", 11), justification="right", size=(10, 1)),
                        sg.Input(key='-DISCOUNT-', readonly=True, justification="right",
                                 disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='0.00',
                                 font=("Helvetica", 11), size=(12, 1)),
                    ],
                    [
                        sg.Text('Invoice Amt:', font=("Helvetica", 11), justification="right", size=(10, 1)),
                        sg.Input(key='-INVOICE-AMT-', readonly=True, justification="right",
                                 disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='0.00',
                                 font=("Helvetica", 11), size=(12, 1)),
                    ],
                    [
                        sg.Text('Paid Amt:', font=("Helvetica", 11), justification="right", size=(10, 1)),
                        sg.Input(key='-PAID-AMT-', readonly=True, justification="right",
                                 disabled_readonly_text_color=disabled_text_color,
                                 disabled_readonly_background_color='gray89', default_text='0.00',
                                 font=("Helvetica", 11), size=(12, 1))
                    ]

                ], size=(col2_w, 220), vertical_alignment='top', pad=None)
        ],
        [
            sg.Column(
                [
                    [
                        sg.Button('↑', size=(4, 2), font='Calibri 12 bold', key='UP', button_color=pad_button_color),
                        sg.Button('7', size=(4, 2), font='Calibri 12 bold', key='T7', button_color=pad_button_color),
                        sg.Button('8', size=(4, 2), font='Calibri 12 bold', key='T8', button_color=pad_button_color),
                        sg.Button('9', size=(4, 2), font='Calibri 12 bold', key='T9', button_color=pad_button_color),

                    ],
                    [
                        sg.Button('↓', size=(4, 2), font='Calibri 12 bold', key='DOWN', button_color=pad_button_color),
                        sg.Button('4', size=(4, 2), font='Calibri 12 bold', key='T4', button_color=pad_button_color),
                        sg.Button('5', size=(4, 2), font='Calibri 12 bold', key='T5', button_color=pad_button_color),
                        sg.Button('6', size=(4, 2), font='Calibri 12 bold', key='T6', button_color=pad_button_color),
                    ],
                    [
                        sg.Button('→', size=(4, 2), font='Calibri 12 bold', key='RIGHT', button_color=pad_button_color),
                        sg.Button('1', size=(4, 2), font='Calibri 12 bold', key='T1', button_color=pad_button_color),
                        sg.Button('2', size=(4, 2), font='Calibri 12 bold', key='T2', button_color=pad_button_color),
                        sg.Button('3', size=(4, 2), font='Calibri 12 bold', key='T3', button_color=pad_button_color),

                    ],
                    [
                        sg.Button('←', size=(4, 2), font='Calibri 12 bold', key='LEFT', button_color=pad_button_color),
                        sg.Button('0', size=(4, 2), font='Calibri 12 bold', key='T0', button_color=pad_button_color),
                        sg.Button('ENT', size=(10, 2), font='Calibri 12 bold', key='ENTER',
                                  button_color=pad_button_color),
                    ],
                    [
                        sg.Button('<<', size=(4, 2), font='Calibri 12 bold', key='BACK-SPACE',
                                  button_color=pad_button_color),
                        sg.Button('.', size=(4, 2), font='Calibri 12 bold', key='FULL-STOP',
                                  button_color=pad_button_color),
                        sg.Button('TAB', size=(10, 2), font='Calibri 12 bold', key='TAB',
                                  button_color=pad_button_color),
                    ],
                ], size=(col2_w, 290), background_color='gray80', vertical_alignment='top', pad=None)
        ],
        [
            sg.Column(
                [
                    [
                        sg.Image(filename='valign-pos.gif')
                    ]
                ], size=(col2_w, 63), vertical_alignment='top', pad=None)
        ]
    ]

    layout_main = [
        [
            sg.Column(layout_column_1, background_color='gray80', vertical_alignment='top', pad=None),

            sg.Column(layout_column_2, background_color='gray80', vertical_alignment='top', pad=None),
        ]
    ]
"""