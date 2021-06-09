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
    # win_w = win_w - 100
    # win_h = win_h - 100

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
    font_size = int(8)
    input_size = int(12)
    table_column_size = [8, 8, 18, 5, 5, 7, 7, 7, 7, 7]
    row_height = 20
    item_rows = 30
    col_height = 50
    num_key_h = 290
    sum_items_h = 220
    if win_w > 1250:
        col1 = int(win_w) - int((win_w * 25 / 100))
        col2 = int((win_w * 25 / 100))
        element_w = 10
        element_h = 2
        font_size = int(12)
        input_size = int(12)
        table_column_size = [13, 13, 24, 6, 6, 8, 8, 8, 8]
        row_height = 25
        col_height = 60
        num_key_h = win_h - 500
        sum_items_h = 240

    col1_size = (col1, col_height)
    inner_col1_w = int((col1 * 70 / 100))
    inner_col2_w = int((col1 * 30 / 100))
    print('col_split_size=', inner_col1_w, inner_col2_w)
    col1_w = col1
    tab_h = (win_h - 420)
    col2_w = col2

    btn_pad_pg: dict = {'size': (4, 2), 'font': ('Helvetica 11 bold'), 'button_color': ("sky blue")}
    btn_pad: dict = {'size': (4, 2), 'font': ('Helvetica 11 bold'), 'button_color': ("sky blue")}
    input_fld: dict = {'readonly': 'True', 'disabled_readonly_text_color': 'gray',
                       'disabled_readonly_background_color': 'gray89', 'font': ("Helvetica", input_size),
                       'size': (input_size, 1)}
    input_fld_font: dict = {'font': ("Helvetica", input_size), 'size': (input_size, 1)}

    input_font: dict = {'font': (f'Helvetica {font_size}'), 'justification': 'right', 'size': (font_size, 1),
                        'pad': ((0, 0), (0, 0))}
    btm_btn: dict = {'size': (font_size, 2), 'font': f'Helvetica {font_size} bold'}
    sum_info: dict = {'readonly': True, 'disabled_readonly_text_color': 'gray',
                      'disabled_readonly_background_color': 'gray89', 'font': ("Helvetica", input_size),
                      'size': (input_size, 1)}
    sum_info_font: dict = {'font': (f'Helvetica {font_size}'), 'justification': 'right', 'size': (input_size, 1)}
    inv_label_font: dict = {'size': (font_size, 1), 'font': ('Helvetica 20'), 'justification': 'left'}
    btn_ent: dict = {'size': (element_w, element_h), 'font': 'Helvetica 11 bold', 'button_color': 'cornflower blue'}

    def col1(self):
        return [
            [
                sg.Column(
                    [
                        [
                            sg.Text('Invoice Entry', **self.inv_label_font),
                            sg.Text('User Name:', **self.input_font),
                            sg.Input(key='-USERID-', **self.input_fld),
                            sg.Text('Terminal:', **self.input_font),
                            sg.Input(key='-TERMINAL-', **self.input_fld),
                            sg.Text('Date:', **self.input_font),
                            sg.Input(key='-DATE-', **self.input_fld, default_text=self.today.strftime("%m/%d/%y"))
                        ]
                    ], size=self.col1_size, vertical_alignment='top')
            ],
            [
                sg.Column(
                    [
                        [
                            sg.Text('Invoice No:', **self.input_font),
                            sg.Input(key='-INVOICE_NO-', **self.input_fld),
                            sg.Text('Reference No:', **self.input_font),
                            sg.Input(key='-REFERENCE_NO-', **self.input_fld),
                            sg.Text('Mobile No:', **self.input_font),
                            sg.Input(key='-MOBILE_NO-', **self.input_fld),
                            sg.Text(key='-STATUS-', size=(7, 1), font=("Helvetica", 15))
                        ]
                    ], size=self.col1_size, vertical_alignment='top')
            ],
            [
                sg.Column(
                    [
                        [
                            sg.Text('Barcode:', **self.input_font),
                            sg.Input(key='-BARCODE-NB-', **self.input_fld_font, enable_events=True),
                            sg.Text('Item Name:', **self.input_font),
                            sg.Input(key='-ITEMNAME-', **self.input_fld_font),
                            sg.Button('BEGN\nHome', size=(6, 2), font=f'Calibri {self.font_size} bold', key='BEGN',
                                      button_color=self.pad_button_color),
                            sg.Button('PREV\nPgUp', size=(6, 2), font=f'Calibri {self.font_size} bold', key='PREV',
                                      button_color=self.pad_button_color),
                            sg.Button('NEXT\nPgDn', size=(6, 2), font=f'Calibri {self.font_size} bold', key='NEXT',
                                      button_color=self.pad_button_color),
                            sg.Button('END\nEnd', size=(6, 2), font=f'Calibri {self.font_size} bold', key='END',
                                      button_color=self.pad_button_color)

                        ]
                    ], size=self.col1_size, vertical_alignment='top')
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
                                     num_rows=self.item_rows,
                                     col_widths=self.table_column_size,
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
                            sg.Button('F1\nHelp', border_width=2, **self.btm_btn, key='F1'),
                            sg.Button('Del Item\nF2', border_width=2, **self.btm_btn, key='F2'),
                            sg.Button('Find Item\nF3', border_width=2, **self.btm_btn, key='F3'),
                            sg.Button('Change Qty\nF4', border_width=2, **self.btm_btn, key='F4'),
                            sg.Button('Change Price\nF5', border_width=2, **self.btm_btn, key='F5'),
                            sg.Button('Get Weight\nF6', border_width=2, **self.btm_btn, key='F6')
                        ],
                        [
                            sg.Button('New Invoice\nF7', border_width=2, **self.btm_btn, key='F7'),
                            sg.Button('Delete Invoice\nF8', border_width=2, **self.btm_btn, key='F8'),
                            sg.Button('Find Custtomer\nF9', border_width=2, **self.btm_btn, key='F9'),
                            sg.Button('List Invoices\nF10', border_width=2, **self.btm_btn, key='F10'),
                            sg.Button('Print Invoices\nF11', border_width=2, **self.btm_btn, key='F11'),
                            sg.Button('Payment\nF12', border_width=2, **self.btm_btn, key='F12'),
                            sg.Button('Exit\nEsc', border_width=2, **self.btm_btn, key='ESC')

                        ]
                    ], size=(self.col1_w, 150), vertical_alignment='top')
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
                    ], size=(self.col2_w, 90), vertical_alignment='top', element_justification='right')
            ],
            [
                sg.Column(
                    [
                        [
                            sg.Text('Line Items:', **self.sum_info_font),
                            sg.Input(key='-LINE-ITEMS-', **self.sum_info)
                        ],
                        [
                            sg.Text('Total Qty:', **self.sum_info_font),
                            sg.Input(key='-TOTAL-QTY-', **self.sum_info)
                        ],
                        [
                            sg.Text('Total Amount:', **self.sum_info_font),
                            sg.Input(key='-TOTAL-PRICE-', **self.sum_info),
                        ],
                        [
                            sg.Text('CGST:', font=("Helvetica", 11), justification="right", size=(10, 1),
                                    visible=False),
                            sg.Input(key='-TOTAL-CGST-', **self.sum_info, visible=False),
                        ],
                        [
                            sg.Text('SGST:', font=("Helvetica", 11), justification="right", size=(10, 1),
                                    visible=False),
                            sg.Input(key='-TOTAL-SGST-', **self.sum_info, visible=False),
                        ],
                        [
                            sg.Text('Tax:', **self.sum_info_font),
                            sg.Input(key='-TOTAL-TAX-', **self.sum_info),
                        ],
                        [
                            sg.Text('Net Amount:', **self.sum_info_font),
                            sg.Input(key='-NET-PRICE-', **self.sum_info),
                        ],
                        [
                            sg.Text('Discount:', **self.sum_info_font),
                            sg.Input(key='-DISCOUNT-', **self.sum_info),
                        ],
                        [
                            sg.Text('Invoice Amt:', **self.sum_info_font),
                            sg.Input(key='-INVOICE-AMT-', **self.sum_info),
                        ],
                        [
                            sg.Text('Paid Amt:', **self.sum_info_font),
                            sg.Input(key='-PAID-AMT-', **self.sum_info)
                        ]
                    ], size=(self.col2_w, self.sum_items_h), vertical_alignment='top')
            ],
            [
                sg.Column(
                    [
                        [
                            sg.Button('\u2191', **self.btn_pad, key='UP'),
                            sg.Button('7', **self.btn_pad, key='T7'),
                            sg.Button('8', **self.btn_pad, key='T8'),
                            sg.Button('9', **self.btn_pad, key='T9'),

                        ],
                        [
                            sg.Button('\u2193', **self.btn_pad, key='DOWN'),
                            sg.Button('4', **self.btn_pad, key='T4'),
                            sg.Button('5', **self.btn_pad, key='T5'),
                            sg.Button('6', **self.btn_pad, key='T6'),
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
                    ], size=(self.col2_w, self.num_key_h), vertical_alignment='top', element_justification='center')
            ],
            [
                sg.Column(
                    [
                        [
                            sg.Image(filename='valign-pos.GIF')
                        ]
                    ], size=(self.col2_w, 63), vertical_alignment='top', element_justification='right')
            ]
        ]

    def layout_chg_qty(self,row_item, list_items):
        return [
            [sg.Text(str(list_items[row_item][2]), size=(30, 2), font=("Helvetica Bold", 12))],
            [sg.Text('Existing Quantity:', size=(15, 1), font=("Helvetica", 11)),
             sg.Input(key='-EXISTING-QTY-', readonly=True, background_color='gray89',
                      disabled_readonly_text_color=InvoiceLayout.disabled_text_color, font=("Helvetica", 11),
                      size=(15, 1))],
            [sg.Text('New Quantity:', size=(15, 1), font=("Helvetica", 11)),
             sg.Input(key='-NEW-QTY-', readonly=False, focus=True, background_color='white', font=("Helvetica", 11),
                      size=(15, 1), enable_events=True)],
            [sg.Text('')],
            [sg.Button('Ok-F12', size=(8, 1), font='Calibri 12 bold', key='-CHG-QTY-OK-',
                       button_color=InvoiceLayout.pad_button_color),
             sg.Button('Esc-Exit', size=(8, 1), font='Calibri 12 bold', key='-CHG-QTY-ESC-',
                       button_color=InvoiceLayout.pad_button_color)]
        ]

    def search_items_layout(self, itemNames):
        return [
            [sg.Text('Search Item:')],
            [sg.In(key='_INPUT_', size=(100, 1))],
            [sg.Listbox(itemNames, size=(100, 10), key='_COMBO_', change_submits=True)],
            [sg.Button('F12-Ok'), sg.Button('Esc-Exit')]
        ]


    def payment_layout(self):
        return [
        [sg.Text('Mobile No.:', size=(8,1),  font=("Helvetica", 11)),
         sg.Input(key='-MOBILE-NO-',readonly=False, focus=True, background_color='white',font=("Helvetica", 11),size=(12,1), enable_events=True),
         sg.Input(key='-CUST-NAME-',readonly=True, focus=False, background_color='gray89', disabled_readonly_text_color=self.disabled_text_color,font=("Helvetica", 11),size=(25,1), enable_events=True)],
        [sg.Text('', size=(8,1))],

        [sg.Column([
            [sg.Text('Net Amount:', size=(12,1),  font=("Helvetica", 11)),
             sg.Input(key='-NET-AMT-',readonly=True, focus=False, background_color='gray89', disabled_readonly_text_color=self.disabled_text_color, font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text('Rounding Adjust:', size=(12,1),  font=("Helvetica", 11)),
             sg.Input(key='-ROUND-ADJ-',readonly=True, focus=True, background_color='gray89', disabled_readonly_text_color=self.disabled_text_color, font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text('Rounded Amt:', size=(12,1),  font=("Helvetica", 11)),
             sg.Input(key='-ROUNDED-AMT-',readonly=True, focus=True, background_color='gray89', disabled_readonly_text_color=self.disabled_text_color, font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text('Discount:', size=(12,1),  font=("Helvetica", 11)),
             sg.Input(key='-DISCOUNT-AMT-',readonly=False, focus=True, background_color='white',font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text('Redeem Pts:', size=(12,1),  font=("Helvetica", 11)),
             sg.Input(key='-REDEEM-PT-',readonly=False, focus=True, background_color='white',font=("Helvetica", 11),justification="right",size=(4,1), enable_events=True),
             sg.Text('Tot:',font=("Helvetica", 11), size=(3,1)),
             sg.Input(key='-AVAILABLE-PT-',readonly=True, focus=True, background_color='gray89', disabled_readonly_text_color=self.disabled_text_color, font=("Helvetica", 11),justification="right",size=(4,1), enable_events=True)],
            ], vertical_alignment='Top'),
        sg.Column([
            [sg.Text('Invoice Amount:', size=(12,1),  font=("Helvetica", 11)),
             sg.Input(key='-INVOICE-AMT-',readonly=True, focus=True, background_color='gray89', disabled_readonly_text_color=self.disabled_text_color, font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
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
             sg.Input(key='-REDEEM-AMT-',readonly=False, focus=False, background_color='gray89', disabled_readonly_text_color=self.disabled_text_color,font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text('Total Payment:', size=(12,1),  font=("Helvetica", 11)),
             sg.Input(key='-TOTAL-PAYMENT-',readonly=False, focus=False, background_color='gray89', disabled_readonly_text_color=self.disabled_text_color,font=("Helvetica", 11),justification="right",size=(15,1), enable_events=True)],
            [sg.Text(' Balance:', size=(10,1),  font=("Helvetica bold", 14)),
             sg.Input(key='-BALANCE-AMT-',readonly=False, focus=False, background_color='gray89', disabled_readonly_text_color=self.disabled_text_color,font=("Helvetica bold", 14),justification="right",size=(11,1), enable_events=True),
             sg.Button('Paid-F2', size=(7, 1), font='Calibri 12 bold', key='-PAID-', button_color = 'orange')],
            ], vertical_alignment='Top'),
        ],
        [sg.Text('', size=(8,1))],
        [sg.Button('OK\nF12', size=(8, 2), font='Calibri 12 bold', key='-PAYMENT-OK-', button_color = self.pad_button_color),
         sg.Button('Exit\nEsc', size=(8, 2), font='Calibri 12 bold', key='-PAYMENT-ESC-', button_color = self.pad_button_color)]
    ]
