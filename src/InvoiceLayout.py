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
    fontsize = int(8)
    inputsize = int(10)
    tablecolumnsize = [8, 8, 18, 5, 5, 7, 7, 7, 7, 7]
    row_height = 20
    col_height = 50
    if win_w > 1250:
        element_w = 15
        element_h = 2
        fontsize = int(12)
        inputsize = int(12)
        tablecolumnsize = [12, 12, 20, 10, 10, 10, 10, 10, 10],
        row_height = 25
        col_height = 50

    col1_size = (col1, col_height)
    inner_col1_w = int((col1 * 70 / 100))
    inner_col2_w = int((col1 * 30 / 100))
    print('col_split_size=',inner_col1_w,inner_col2_w)
    col1_w = col1
    tab_h = 350
    col2_w = col2

    btn_pad_pg: dict = {'size': (4, 2), 'font': ('Helvetica 11 bold'), 'button_color': ("sky blue")}
    btn_pad: dict = {'size': (4, 2), 'font': ('Helvetica 11 bold'), 'button_color': ("sky blue")}
    input_fld: dict = {'readonly': 'True', 'disabled_readonly_text_color': 'gray',
                       'disabled_readonly_background_color': 'gray89', 'font': ("Helvetica", inputsize), 'size': (inputsize, 1)}
    input_fld_font: dict = {'font': ("Helvetica", inputsize), 'size': (inputsize, 1)}

    input_font: dict = {'font': (f'Helvetica {fontsize}'),'justification': 'right', 'size': (12,1)}
    btm_btn: dict = {'size': (10, 2), 'font': f'Helvetica {fontsize} bold'}
    sum_info: dict = {'readonly': True, 'disabled_readonly_text_color': 'gray',
                      'disabled_readonly_background_color': 'gray89', 'font': ("Helvetica", inputsize), 'size': (inputsize, 1)}
    sum_info_font: dict = {'font': (f'Helvetica {fontsize}'), 'justification': 'right', 'size': (inputsize, 1)}
    inv_label_font: dict = {'size': (10, 1), 'font': ('Helvetica 20'), 'justification': 'left'}
    btn_ent: dict = {'size': (element_w, element_h), 'font': 'Helvetica 11 bold', 'button_color': 'cornflower blue'}

    def col1(self):
         return [
                [
                    sg.Column(
                        [
                            [
                                sg.Text('User Name:', **self.input_font),
                                sg.Input(key='-USERID-', **self.input_fld),
                                sg.Text('Terminal:', **self.input_font),
                                sg.Input(key='-TERMINAL-', **self.input_fld),
                                sg.Text('Date:', **self.input_font),
                                sg.Input(key='-DATE-', **self.input_fld,default_text=self.today.strftime("%m/%d/%y")),
                                sg.Text('Invoice Entry', **self.inv_label_font)
                            ]
                            ], size=self.col1_size, vertical_alignment='center')
                ],
                [
                    sg.Column(
                        [
                            [
                                sg.Text('Invoice No:', **self.input_font),
                                sg.Input(key='-INVOICE_NO-',**self.input_fld),
                                sg.Text('Reference No:', **self.input_font),
                                sg.Input(key='-REFERENCE_NO-', **self.input_fld),
                                sg.Text('Customer:', **self.input_font),
                                sg.Input(key='-CUSTOMER-', **self.input_fld),
                                sg.Text('Mobile No:', **self.input_font),
                                sg.Input(key='-MOBILE_NO-', **self.input_fld)
                            ]
                        ], size=self.col1_size, vertical_alignment='center')
                ],
                [
                    sg.Column(
                        [
                            [
                                sg.Text('Barcode:', **self.input_font),
                                sg.Input(key='-BARCODE-NB-', **self.input_fld_font, enable_events = True),
                                sg.Text('Item Name:', **self.input_font),
                                #sg.InputCombo(('8901314010322'), background_color='White' ,auto_size_text=True, font=("Helvetica", 12),
                                #              size=(20, 20), key='Item-Name' ),
                                sg.Input(key='-ITEMNAME-', **self.input_fld_font),
                                sg.Button('Search Item', border_width=2,size=(10,1),font='Helvetica 8 bold' ,key='-SEARCH-ITME-'),
                                sg.Text('UNPAID', font=("Helvetica", self.fontsize)),
                                sg.Button('PREV\n←', size=(6, 2), font=f'Calibri {self.fontsize} bold',
                                          key='PREV',
                                          button_color=self.pad_button_color),
                                sg.Button('NEXT\n→', size=(6, 2), font=f'Calibri {self.fontsize} bold',
                                          key='NEXT',
                                          button_color=self.pad_button_color)
                            ]
                        ], size=self.col1_size, vertical_alignment='center')
                ],
                [
                    sg.Column(
                        [
                            [
                                sg.Table(values=self.data,
                                         key='-TABLE-',
                                         headings=self.column_heading,
                                         font=(("Helvetica", 11)),
                                         # max_col_width=500,
                                         auto_size_columns=False,
                                         justification='right',
                                         row_height={self.row_height},
                                         alternating_row_color='lightsteelBlue1',
                                         num_rows=15,
                                         col_widths=self.tablecolumnsize,
                                         enable_events=True,
                                         bind_return_key=True
                                         )
                            ]
                        ], size=(self.col1_w, self.tab_h))
                ],
                [
                    sg.Column(
                        [
                            [
                                sg.Button('F1\nHelp', border_width=2,**self.btm_btn , key='F1'),
                                sg.Button('F2\nDel Item', border_width=2, **self.btm_btn, key='F2'),
                                sg.Button('F3\nLookup', border_width=2, **self.btm_btn, key='F3'),
                                sg.Button('F4\nChange Qty', border_width=2, **self.btm_btn, key='F4'),
                                sg.Button('F5\nChange Price', border_width=2, **self.btm_btn, key='F5'),
                                sg.Button('F6\nGet Weight', border_width=2, **self.btm_btn, key='F6')
                            ],
                            [
                                sg.Button('F7\nNew Invoice',border_width=2, **self.btm_btn, key='F7'),
                                sg.Button('F8\nDel Invoice', border_width=2 ,**self.btm_btn, key='F8'),
                                sg.Button('F9\nLookup Cust', border_width=2,**self.btm_btn, key='F9'),
                                sg.Button('F10\nList Invoices', border_width=2,**self.btm_btn, key='F10'),
                                sg.Button('F11\nPrint Invoices', border_width=2,**self.btm_btn, key='F11'),
                                sg.Button('F12\nPayment', border_width=2,**self.btm_btn, key='F12'),
                                sg.Button('Esc-Exit', border_width=2,**self.btm_btn, key='ESC')

                            ]
                        ], size=(self.col1_w, 150), vertical_alignment='center')
                ]
            ]

    def col2(self):
        return [
            [
                sg.Column(
                    [
                        [
                            sg.Image(filename='company-logo.GIF')
                        ]
                    ], size=(self.col2_w, 90), vertical_alignment='top')
            ],
            [
                sg.Column(
                    [
                        [
                            sg.Text('Line Items:',  **self.sum_info_font),
                            sg.Input(key='-LINE-ITEMS-', **self.sum_info)
                        ],
                        [
                            sg.Text('Total Qty:',  **self.sum_info_font),
                            sg.Input(key='-TOTAL-QTY-',**self.sum_info)
                        ],
                        [
                            sg.Text('Total Price:',  **self.sum_info_font),
                            sg.Input(key='-TOTAL-PRICE-', **self.sum_info),
                        ],
                        [
                            sg.Text('Tax:',  **self.sum_info_font),
                            sg.Input(key='-TOTAL-TAX-',**self.sum_info),
                        ],
                        [
                            sg.Text('Net Price:',  **self.sum_info_font),
                            sg.Input(key='-NET-PRICE-', **self.sum_info),
                        ],
                        [
                            sg.Text('Discount:',  **self.sum_info_font),
                            sg.Input(key='-DISCOUNT-', **self.sum_info),
                        ],
                        [
                            sg.Text('Invoice Amt:',  **self.sum_info_font),
                            sg.Input(key='-INVOICE-AMT-', **self.sum_info),
                        ],
                        [
                            sg.Text('Paid Amt:',  **self.sum_info_font),
                            sg.Input(key='-PAID-AMT-', **self.sum_info)
                        ]
                    ], size=(self.col2_w, 220), vertical_alignment='top')
            ],
            [
                sg.Column(
                    [
                        [
                            sg.Button('\u2191', **self.btn_pad , key='UP'),
                            sg.Button('7', **self.btn_pad , key='T7'),
                            sg.Button('8', **self.btn_pad , key='T8'),
                            sg.Button('9', **self.btn_pad , key='T9'),

                        ],
                        [
                            sg.Button('\u2193', **self.btn_pad ,key='DOWN'),
                            sg.Button('4', **self.btn_pad ,key='T4' ),
                            sg.Button('5', **self.btn_pad ,key='T5' ),
                            sg.Button('6', **self.btn_pad , key='T6' ),
                        ],
                        [
                            sg.Button('\u2192', **self.btn_pad, key='RIGHT'),
                            sg.Button('1', **self.btn_pad, key='T1'),
                            sg.Button('2', **self.btn_pad, key='T2'),
                            sg.Button('3', **self.btn_pad, key='T3'),

                        ],
                        [
                            sg.Button('\u2190', **self.btn_pad, key='LEFT'),
                            sg.Button('0', **self.btn_pad, key='T0'),
                            sg.Button('Enter', **self.btn_ent, key='ENTER'),
                        ],
                        [
                            sg.Button('<<', **self.btn_pad_pg, key='BACK-SPACE'),
                            sg.Button('Dn', **self.btn_pad_pg, key='TPD'),
                            sg.Button('.', **self.btn_pad, key='FULL-STOP'),
                            sg.Button('TAB', **self.btn_pad, key='TAB')
                        ]
                    ], size=(self.col2_w, 290), vertical_alignment='top')
            ],
            [
                sg.Column(
                    [
                        [
                            sg.Image(filename='valign-pos.GIF')
                        ]
                    ], size=(self.col2_w, 63), vertical_alignment='center', justification='center')
            ]
        ]

    def layout_chg_qty(self,list_item):
        return [
            [sg.Text(str(list_item[2]), size=(30, 2), font=("Helvetica Bold", 12))],
            [sg.Text('Existing Quantity:', size=(15, 1), font=("Helvetica", 11)),
             sg.Input(key='-EXISTING-QTY-', readonly=True, background_color='gray89',
                      disabled_readonly_text_color=InvoiceLayout.disabled_text_color, font=("Helvetica", 11),
                      size=(15, 1))],
            [sg.Text('New Quantity:', size=(15, 1), font=("Helvetica", 11)),
             sg.Input(key='-NEW-QTY-', readonly=False, focus=True, background_color='white', font=("Helvetica", 11),
                      size=(15, 1), enable_events=True)],
            [sg.Text('')],
            [sg.Button('F12-Ok', size=(8, 1), font='Calibri 12 bold', key='-CHG-QTY-OK-',
                       button_color=InvoiceLayout.pad_button_color),
             sg.Button('Esc-Exit', size=(8, 1), font='Calibri 12 bold', key='-CHG-QTY-ESC-',
                       button_color=InvoiceLayout.pad_button_color)]
        ]


    def search_items_layout(self,itemNames):
        return [
                    [sg.Text('Search Item:')],
                    [sg.In(key='_INPUT_', size=(100, 1))],
                    [sg.Listbox(itemNames, size=(100, 10), key='_COMBO_', change_submits=True)],
                    [sg.Button('F12-Ok'), sg.Button('Esc-Exit')]
                ]
