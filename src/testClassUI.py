import PySimpleGUI as sg
import datetime


######
class TestClassUI:

    sg.theme('DefaultNoMoreNagging')
    pad_button_color = 'SteelBlue3'    
    function_button_color = 'SteelBlue3'
    readonly_text_color = 'grey32'
    readonly_background_color = 'grey89'
    
    pane_detail_column_heading =['Item code', 'Barcode', 'Item Name', 'Unit', 'Qty', 'Price', 'Amount', 'Tax Rate', 'Tax', 'Net']

    layout_pane_title = [
        [
            sg.Column(
            [
                [
                    sg.Text('Invoice Entry', size=(36,1) ,font=("Helvetica", 18)),
                    sg.Text('User:', font=("Helvetica", 10)),
                    sg.Input(key='_USER_ID_', font=("Helvetica", 10),size=(15,1),readonly=True, disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color),
                    sg.Text('Terminal:',font=("Helvetica", 10)),
                    sg.Input(key='_TERMINAL_ID_', font=("Helvetica", 10),size=(4,1),readonly=True, disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color),
                    sg.Text('Date:',font=("Helvetica", 10)),
                    sg.Input(key='_CURRENT_DATE_', font=("Helvetica", 10),size=(10,1),readonly=True, disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color),
                ]
            ])
        ]
    ]

    layout_pane_header = [
        [
            sg.Column(
            [
                [
                    sg.Text('Invoice No:', size=(8,1),  font=("Helvetica", 12)),
                    sg.Input(key='_INVOICE_NUMBER_',readonly=True, disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color ,default_text='' ,font=("Helvetica", 12),size=(10,1)),
                    sg.Text('Reference No:', size=(8,1),  font=("Helvetica", 12)),
                    sg.Input(key='_REFERENCE_NUMBER_',readonly=True, disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color ,default_text='' ,font=("Helvetica", 12),size=(10,1)),
                    sg.Text('Mobile No:', size=(8,1),  font=("Helvetica", 12)),
                    sg.Input(key='_MOBILE_NUMBER_',readonly=True, disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color ,default_text='' ,font=("Helvetica", 12),size=(15,1)),
                    sg.Input(key='_PAYMENT_STATUS_',readonly=True, disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color='gray95' ,default_text='' ,font=("Helvetica", 16), border_width = 0, size=(9,1)),
                    sg.Button('BEGN\nHome', size=(5, 2), font='Calibri 11 bold', key='_BEGIN_', button_color = pad_button_color),
                    sg.Button('PREV\nPgUp', size=(5, 2), font='Calibri 11 bold', key='_PREVIOUS_', button_color = pad_button_color),
                    sg.Button('NEXT\nPgDn', size=(5, 2), font='Calibri 11 bold', key='_NEXT_', button_color = pad_button_color),    
                    sg.Button('END\nEnd', size=(5, 2), font='Calibri 11 bold', key='_END_', button_color = pad_button_color),    
                ]
            ])    
        ]
    ]

    layout_pane_search = [
        [
            sg.Column(
            [
                [
                    sg.Text('Barcode:', size=(8,1),  font=("Helvetica", 12)),
                    sg.Input(key='_BARCODE_',background_color='White',font=("Helvetica", 12),size=(15,1), enable_events = True),
                    sg.Text('Item Name:', size=(9,1), font=("Helvetica", 12), justification='right'),
                    sg.Input(key='_ITEM_NAME_',background_color='White',font=("Helvetica", 12),size=(25,1), enable_events = True),
                ]
            ])   
        ]
    ]
    
    layout_pane_detail = [
        [
            sg.Column(
            [
                [
                    sg.Table(values=[], key='_LIST_ITEMS_', enable_events=True,
                         headings= pane_detail_column_heading,
                         font=(("Helvetica", 11)),
                         auto_size_columns=False,
                         justification='right',
                         row_height=25,
                         alternating_row_color='lightsteelBlue1',
                         num_rows=12,
                         display_row_numbers=True,
                         col_widths=[10, 13, 20, 5, 5, 8, 10, 8, 10, 10]
                    )            
                ]        
            ])    
        ]
    ]

    layout_pane_action = [
        [
            sg.Column(
            [
                [
                    sg.Button('Help\nF1', size=(13, 2), font='Helvetica 11 bold', key='F1', button_color = function_button_color),
                    sg.Button('Delete Item\nF2', size=(13, 2), font='Helvetica 11 bold', key='F2', button_color = function_button_color),
                    sg.Button('Change Quantity\nF3', size=(13, 2), font='Helvetica 11 bold', key='F3', button_color = function_button_color),
                    sg.Button('Change Price\nF4', size=(13, 2), font='Helvetica 11 bold', key='F4', button_color = function_button_color),
                    sg.Button('Get Weight\nF5', size=(13, 2), font='Helvetica 11 bold', key='F5', button_color = function_button_color),
                    sg.Button('Carry Bag\nF6', size=(13, 2), font='Helvetica 11 bold', key='F6', button_color = function_button_color)
                ],
                [
                    sg.Button('New Invoice\nF7', size=(13, 2), font='Helvetica 11 bold', key='F7', button_color = function_button_color),
                    sg.Button('Delete Invoice\nF8', size=(13, 2), font='Helvetica 11 bold', key='F8', button_color = function_button_color),
                    sg.Button('List Invoices\nF9', size=(13, 2), font='Helvetica 11 bold', key='F9', button_color = function_button_color),
                    sg.Button('Print Invoice\nF10', size=(13, 2), font='Helvetica 11 bold', key='F10', button_color = function_button_color),
                    sg.Button('Cash Position\nF11', size=(13, 2), font='Helvetica 11 bold', key='F11', button_color = function_button_color),
                    sg.Button('Payment\nF12', size=(13, 2), font='Helvetica 11 bold', key='F12', button_color = function_button_color),
                    sg.Button('Exit\nEsc', size=(13, 2), font='Helvetica 11 bold', key='ESC', button_color = function_button_color)
                ]               
            ])    
        ]
    ]

    layout_pane_company = [
        [
            sg.Column(
            [
                [
                    sg.Image(filename = 'al-fareeda-logo.PNG', background_color = 'white')
                ]
            ], vertical_alignment = 'top', pad=(45,5), background_color = 'white')
        ]
    ]
    
    layout_pane_summary = [
        [
            sg.Column(
            [
                [
                    sg.Text('Line Items:',  font=("Helvetica", 10) , justification="right", size=(10,1)),
                    sg.Input(key='_LINE_ITEMS_', readonly=True, justification="right", disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color, default_text='0' ,font=("Helvetica", 10), size=(10,1))          
                ],
                [
                    sg.Text('Total Qty:',  font=("Helvetica", 10),justification="right", size=(10,1)),
                    sg.Input(key='_TOTAL_QTY_', readonly=True, justification="right", disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color, default_text='0.00' ,font=("Helvetica", 10), size=(10,1))
                ],
                [
                    sg.Text('Total Amount:',  font=("Helvetica", 10),justification="right", size=(10,1)),
                    sg.Input(key='_TOTAL_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color, default_text='0.00' ,font=("Helvetica", 10),size=(10,1)),
                ],
                [
                    sg.Text('CGST:', font=("Helvetica", 10),justification="right",size=(10,1), visible=False),
                    sg.Input(key='_TOTAL_CGST_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color, default_text='0.00' , font=("Helvetica", 10), size=(10,1), visible=False),
                ],
                [
                    sg.Text('SGST:', font=("Helvetica", 10),justification="right",size=(10,1), visible=False),
                    sg.Input(key='_TOTAL_SGST_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color, default_text='0.00' , font=("Helvetica", 10), size=(10,1), visible=False),
                ],
                [
                    sg.Text('Tax:', font=("Helvetica", 10),justification="right",size=(10,1)),
                    sg.Input(key='_TOTAL_TAX_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color, default_text='0.00' , font=("Helvetica", 10), size=(10,1)),
                ],
                [
                    sg.Text('Net Amount:', font=("Helvetica", 10),justification="right",size=(10,1)),
                    sg.Input(key='_NET_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color, default_text='0.00' , font=("Helvetica", 10), size=(10,1)),
                ],
                [
                    sg.Text('Discount:', font=("Helvetica", 10),justification="right",size=(10,1)),
                    sg.Input(key='_DISCOUNT_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color, default_text='0.00' , font=("Helvetica", 10), size=(10,1)),
                ],
                [
                    sg.Text('Invoice Amt:', font=("Helvetica", 10),justification="right",size=(10,1)),
                    sg.Input(key='_INVOICE_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color, default_text='0.00' ,font=("Helvetica", 10),size=(10,1)),
                ],
                [
                    sg.Text('Paid Amt:', font=("Helvetica", 10),justification="right",size=(10,1)),
                    sg.Input(key='_PAID_AMOUNT_', readonly=True, justification="right", disabled_readonly_text_color=readonly_text_color, disabled_readonly_background_color=readonly_background_color, default_text='0.00' , font=("Helvetica", 10), size=(10,1))
                ]            
                
            ], vertical_alignment = 'top', pad = (18,0))           
        ]
    ]        

    layout_pane_keypad = [
        [
            sg.Column(
            [
                [
                    sg.Button('↑', size=(4, 2), font='Calibri 11 bold', key='UP', button_color = pad_button_color),
                    sg.Button('7', size=(4, 2), font='Calibri 11 bold', key='T7', button_color = pad_button_color),
                    sg.Button('8', size=(4, 2), font='Calibri 11 bold', key='T8', button_color = pad_button_color),
                    sg.Button('9', size=(4, 2), font='Calibri 11 bold', key='T9', button_color = pad_button_color),                
                    
                ],
                [
                    sg.Button('↓', size=(4, 2), font='Calibri 11 bold', key='DOWN', button_color = pad_button_color),
                    sg.Button('4', size=(4, 2), font='Calibri 11 bold', key='T4', button_color = pad_button_color),
                    sg.Button('5', size=(4, 2), font='Calibri 11 bold', key='T5', button_color = pad_button_color),
                    sg.Button('6', size=(4, 2), font='Calibri 11 bold', key='T6', button_color = pad_button_color),                  
                ],
                [
                    sg.Button('→', size=(4, 2), font='Calibri 11 bold', key='RIGHT', button_color = pad_button_color),
                    sg.Button('1', size=(4, 2), font='Calibri 11 bold', key='T1', button_color = pad_button_color),
                    sg.Button('2', size=(4, 2), font='Calibri 11 bold', key='T2', button_color = pad_button_color),
                    sg.Button('3', size=(4, 2), font='Calibri 11 bold', key='T3', button_color = pad_button_color),                
                    
                ],
                [
                    sg.Button('←', size=(4, 2), font='Calibri 11 bold', key='LEFT', button_color = pad_button_color),
                    sg.Button('0', size=(4, 2), font='Calibri 11 bold', key='T0', button_color = pad_button_color),
                    sg.Button('ENT', size=(10, 2), font='Calibri 11 bold', key='ENTER', button_color = pad_button_color),
                ],            
                [
                    sg.Button('\u232B', size=(4, 2), font='Calibri 11 bold', key='BACKSPACE', button_color = pad_button_color),
                    sg.Button('.', size=(4, 2), font='Calibri 11 bold', key='FULL_STOP', button_color = pad_button_color),
                    sg.Button('TAB', size=(10, 2), font='Calibri 11 bold', key='TAB', button_color = pad_button_color),
                ],            
            ], vertical_alignment = 'top', pad = (9,0))    
        ]
    ]        

    layout_pane_logo = [
        [
            sg.Column(
            [
                [
                    sg.Image(filename = 'align-pos-exp1.PNG', background_color = 'white')
                ]
            ], vertical_alignment = 'top', pad = (45,5), background_color = 'white')    
        ]
    ] 
    
    layout_left_panes = [
        [
            sg.Column(layout_pane_title, size = (990,42), vertical_alignment = 'top', pad = None)     
        ],
        [
            sg.Column(layout_pane_header, size = (990,60), vertical_alignment = 'top', pad = None)     
        ],
        [
            sg.Column(layout_pane_search, size = (990,38), vertical_alignment = 'top', pad = None)     
        ],
        [
            sg.Column(layout_pane_detail, size = (990,338), vertical_alignment = 'top', pad = None)     
        ],
        [
            sg.Column(layout_pane_action, size = (990,120), vertical_alignment = 'top', pad = None)     
        ]         
    ]

    layout_right_panes = [
        [
            sg.Column(layout_pane_company, size = (530,75), vertical_alignment = 'top', pad = ((0,0),(0,0)), background_color='White')     
        ],
        [
            sg.Column(layout_pane_summary, size = (530,230), vertical_alignment = 'top', pad = ((3,0),(10,0)), background_color=None)     
        ],
        [
            sg.Column(layout_pane_keypad, size = (530,270), vertical_alignment = 'top', pad = ((12,12),(0,0)), background_color=None)     
        ],
        [
            sg.Column(layout_pane_logo, size = (530,40), vertical_alignment = 'top', pad = ((0,0),(10,0)), background_color='White')     
        ]        
    ]

    layout_main = [
        [
            sg.Column(layout_left_panes, size = (990,700), vertical_alignment = 'top', pad = (0,0), background_color='White'),
            sg.Column(layout_right_panes, size = (530,700), vertical_alignment = 'top', pad = None, background_color=None)   
        ]      
    ]


######
class PaneTitle:

    def __init__(self, window):
        self.__window = window
        self.__user_id = ''
        self.__terminal_id = ''
        self.__current_date = datetime.datetime(1900, 1, 1)
        
        window['_USER_ID_'].Widget.config(takefocus=0)
        window['_TERMINAL_ID_'].Widget.config(takefocus=0)
        window['_CURRENT_DATE_'].Widget.config(takefocus=0)
                
    def set_user_id(self, user_id):
        self.__user_id = user_id
        self.__window.Element('_USER_ID_').update(value = self.__user_id)
        
    def get_user_id(self):
        self.__user_id = self.__window.Element('_USER_ID_').get()
        return self.__user_id
        
    def set_terminal_id(self, terminal_id):
        self.__terminal_id = terminal_id
        self.__window.Element('_TERMINAL_ID_').update(value = self.__terminal_id)        
        
    def get_terminal_id(self):
        self.__terminal_id = self.__window.Element('_TERMINAL_ID_').get()    
        return self.__terminal_id
        
    def set_current_date(self, current_date):
        self.__current_date = current_date
        self.__window.Element('_CURRENT_DATE_').update(value = self.__current_date)        
        
    def get_current_date(self):
        self.__current_date = self.__window.Element('_CURRENT_DATE_').get()        
        return self.__current_date
               
    user_id = property(get_user_id, set_user_id) 
    terminal_id = property(get_terminal_id, set_terminal_id)
    current_date = property(get_current_date, set_current_date)


class PaneHeader:

    def __init__(self, window):
        self.__window = window
        self.__reference_number = str('')
        self.__invoice_number = str('')
        self.__mobile_number = str('')
        self.__payment_status = str('')
        
        window['_REFERENCE_NUMBER_'].Widget.config(takefocus=0)
        window['_INVOICE_NUMBER_'].Widget.config(takefocus=0)
        window['_MOBILE_NUMBER_'].Widget.config(takefocus=0)
        window['_PAYMENT_STATUS_'].Widget.config(takefocus=0)
        window['_BEGIN_'].Widget.config(takefocus=0)
        window['_PREVIOUS_'].Widget.config(takefocus=0)
        window['_NEXT_'].Widget.config(takefocus=0)
        window['_END_'].Widget.config(takefocus=0)


    def set_reference_number(self, reference_number):
        self.__reference_number = reference_number
        self.__window.Element('_REFERENCE_NUMBER_').update(value = self.__reference_number)
        
    def get_reference_number(self):
        self.__reference_number = self.__window.Element('_REFERENCE_NUMBER_').get()        
        return self.__reference_number
        
    def set_invoice_number(self, invoice_number):
        self.__invoice_number = invoice_number
        self.__window.Element('_INVOICE_NUMBER_').update(value = self.__invoice_number)
        
    def get_invoice_number(self):
        self.__invoice_number = self.__window.Element('_INVOICE_NUMBER_').get()        
        return self.__invoice_number
        
    def set_mobile_number(self, mobile_number):
        self.__mobile_number = mobile_number
        self.__window.Element('_MOBILE_NUMBER_').update(value = self.__mobile_number)
        
    def get_mobile_number(self):
        self.__mobile_number = self.__window.Element('_MOBILE_NUMBER_').get()        
        return self.__mobile_number

    def set_payment_status(self, payment_status):
        self.__payment_status = payment_status
        self.__window.Element('_PAYMENT_STATUS_').update(value = self.__payment_status)
        
    def get_payment_status(self):
        self.__payment_status = self.__window.Element('_PAYMENT_STATUS_').get()        
        return self.__payment_status

    reference_number = property(get_reference_number, set_reference_number) 
    invoice_number = property(get_invoice_number, set_invoice_number) 
    mobile_number = property(get_mobile_number, set_mobile_number) 
    payment_status = property(get_payment_status, set_payment_status) 
        

class PaneSearch:

    def __init__(self, window):
        self.__window = window
        self.__barcode = str('')
        self.__item_name = str('')
        
    def set_barcode(self, barcode):
        self.__barcode = barcode
        self.__window.Element('_BARCODE_').update(value = self.__barcode)
        
    def get_barcode(self):
        self.__barcode = self.__window.Element('_BARCODE_').get()        
        return self.__barcode

    def set_item_name(self, item_name):
        self.__item_name = item_name
        self.__window.Element('_ITEM_NAME_').update(value = self.__item_name)
        
    def get_item_name(self):
        self.__item_name = self.__window.Element('_ITEM_NAME_').get()        
        return self.__item_name

    def focus_barcode(self):
        self.__window.Element('_BARCODE_').SetFocus() 

    barcode = property(get_barcode, set_barcode) 
    item_name = property(get_item_name, set_item_name) 


class PaneDetail:

    def __init__(self, window):
        self.__window = window
        self.__list_items = []
        self.__item_code = str('')
        self.__barcode = str('')
        self.__item_name = str('')
        self.__uom = str('')
        self.__qty = float(0.0)
        self.__selling_price = float(0.00)
        self.__selling_amount = float(0.00)
        self.__tax_rate = float(0.00)
        self.__tax_amount = float(0.00)
        self.__net_amount = float(0.00)
        self.__cgst_tax_rate = float(0.00)
        self.__sgst_tax_rate = float(0.00)
        self.__line_item = []       
        
    def set_list_items(self, list_items):
        self.__list_items = list_items
        window.Element('_LIST_ITEMS_').update(values = self.__list_items)
        
    def get_list_items(self):
        self.__list_items = window.Element('_LIST_ITEMS_').get()
        return self.__list_items
              
    def set_item_code(self, item_code):
        self.__item_code = item_code
        
    def get_item_code(self):
        return self.__item_code

    def set_barcode(self, barcode):
        self.__barcode = barcode
        
    def get_barcode(self):
        return self.__barcode

    def set_item_name(self, item_name):
        self.__item_name = item_name
        
    def get_item_name(self):
        return self.__item_name

    def set_uom(self, uom):
        self.__uom = uom
        
    def get_uom(self):
        return self.__uom

    def set_qty(self, qty):
        self.__qty = qty
        
    def get_qty(self):
        return self.__qty

    def set_selling_price(self, selling_price):
        self.__selling_price = selling_price
        
    def get_selling_price(self):
        return self.__selling_price

    def set_selling_amount(self, selling_amount):
        self.__selling_amount = selling_amount
        
    def get_selling_amount(self):
        return self.__selling_amount

    def set_tax_rate(self, tax_rate):
        self.__tax_rate = tax_rate
        
    def get_tax_rate(self):
        return self.__tax_rate

    def set_tax_amount(self, tax_amount):
        self.__tax_amount = tax_amount
        
    def get_tax_amount(self):
        return self.__tax_amount

    def set_net_amount(self, net_amount):
        self.__net_amount = net_amount
        
    def get_net_amount(self):
        return self.__net_amount

    def set_cgst_tax_rate(self, cgst_tax_rate):
        self.__cgst_tax_rate = cgst_tax_rate
        
    def get_cgst_tax_rate(self):
        return self.__cgst_tax_rate

    def set_sgst_tax_rate(self, sgst_tax_rate):
        self.__sgst_tax_rate = sgst_tax_rate
        
    def get_sgst_tax_rate(self):
        return self.__sgst_tax_rate       
                            
    def clear_list_items(self):
        self.__list_items.clear()
        self.__window.Element('_LIST_ITEMS_').update(values = self.__list_items)

    def __elements_to_line_item(self):
        self.__line_item.append(self.__item_code)
        self.__line_item.append(self.__barcode)        
        self.__line_item.append(self.__item_name)        
        self.__line_item.append(self.__uom)        
        self.__line_item.append("{:.2f}".format(self.__qty))        
        self.__line_item.append("{:.2f}".format(self.__selling_price))        
        self.__line_item.append("{:.2f}".format(self.__selling_amount))       
        self.__line_item.append("{:.2f}".format(self.__tax_rate))     
        self.__line_item.append("{:.2f}".format(self.__tax_amount))       
        self.__line_item.append("{:.2f}".format(self.__net_amount))    
        self.__line_item.append("{:.2f}".format(self.__cgst_tax_rate))       
        self.__line_item.append("{:.2f}".format(self.__sgst_tax_rate))
       
    def add_line_item(self):
        self.__line_item = []
        self.__elements_to_line_item()    
        self.__list_items.append(self.__line_item)
        self.__window.Element('_LIST_ITEMS_').update(values = self.__list_items)

    def update_line_item(self, idx):
        self.__line_item = []
        self.__elements_to_line_item()                        
        self.__list_items[idx] = self.__line_item
        self.__window.Element('_LIST_ITEMS_').update(values = self.__list_items)

    def delete_line_item(self, idx):
        self.__list_items.pop(idx)
        self.__window.Element('_LIST_ITEMS_').update(values = self.__list_items)

    list_items = property(get_list_items, set_list_items)
    item_code = property(get_item_code, set_item_code)
    barcode = property(get_barcode, set_barcode)
    item_name = property(get_item_name, set_item_name)
    uom = property(get_uom, set_uom)
    qty = property(get_qty, set_qty)
    selling_price = property(get_selling_price, set_selling_price)
    selling_amount = property(get_selling_amount, set_selling_amount)
    tax_rate = property(get_tax_rate, set_tax_rate)
    tax_amount = property(get_tax_amount, set_tax_amount)
    net_amount = property(get_net_amount, set_net_amount)
    cgst_tax_rate = property(get_cgst_tax_rate, set_cgst_tax_rate)
    sgst_tax_rate = property(get_sgst_tax_rate, set_sgst_tax_rate)


class PaneAction:

    def __init__(self, window):
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


class PaneSummary:

    def __init__(self, window):
        self.__window = window
        self.__line_items = 0
        self.__total_qty = float(0.00)
        self.__total_amount = float(0.00)
        self.__total_tax_amount = float(0.00)
        self.__total_cgst_amount = float(0.00)
        self.__total_sgst_amount = float(0.00)
        self.__net_amount = float(0.00)
        self.__discount_amount = float(0.00)
        self.__invoice_amount = float(0.00)
        self.__paid_amount = float(0.00)
        window['_LINE_ITEMS_'].Widget.config(takefocus=0)
        window['_TOTAL_QTY_'].Widget.config(takefocus=0)
        window['_TOTAL_AMOUNT_'].Widget.config(takefocus=0)
        window['_TOTAL_TAX_AMOUNT_'].Widget.config(takefocus=0)
        window['_TOTAL_CGST_AMOUNT_'].Widget.config(takefocus=0)
        window['_TOTAL_SGST_AMOUNT_'].Widget.config(takefocus=0)
        window['_NET_AMOUNT_'].Widget.config(takefocus=0)
        window['_DISCOUNT_AMOUNT_'].Widget.config(takefocus=0)
        window['_INVOICE_AMOUNT_'].Widget.config(takefocus=0)
        window['_PAID_AMOUNT_'].Widget.config(takefocus=0)

    def set_line_items(self, line_items):
        self.__line_items = line_items
        self.__window.Element('_LINE_ITEMS_').update(value = self.__line_items)
        
    def get_line_items(self):
        self.__line_items = self.__window.Element('_LINE_ITEMS_').get()        
        return self.__line_items
        
    def set_total_qty(self, total_qty):
        self.__total_qty = total_qty
        self.__window.Element('_TOTAL_QTY_').update(value = self.__total_qty)
        
    def get_total_qty(self):
        self.__total_qty = self.__window.Element('_TOTAL_QTY_').get()        
        return self.__total_qty

    def set_total_amount(self, total_amount):
        self.__total_amount = total_amount
        self.__window.Element('_TOTAL_AMOUNT_').update(value = "{:.2f}".format(self.__total_amount))
        
    def get_total_amount(self):
        self.__total_amount = self.__window.Element('_TOTAL_AMOUNT_').get()        
        return self.__total_amount

    def set_total_tax_amount(self, total_tax_amount):
        self.__total_tax_amount = total_tax_amount
        self.__window.Element('_TOTAL_TAX_AMOUNT_').update(value = "{:.2f}".format(self.__total_tax_amount))
        
    def get_total_tax_amount(self):
        self.__total_tax_amount = self.__window.Element('_TOTAL_TAX_AMOUNT_').get()        
        return self.__total_tax_amount

    def set_total_cgst_amount(self, total_cgst_amount):
        self.__total_cgst_amount = total_cgst_amount
        self.__window.Element('_TOTAL_CGST_AMOUNT_').update(value = "{:.2f}".format(self.__total_cgst_amount))
        
    def get_total_cgst_amount(self):
        self.__total_cgst_amount = self.__window.Element('_TOTAL_CGST_AMOUNT_').get()        
        return self.__total_cgst_amount

    def set_total_sgst_amount(self, total_sgst_amount):
        self.__total_sgst_amount = total_sgst_amount
        self.__window.Element('_TOTAL_SGST_AMOUNT_').update(value = "{:.2f}".format(self.__total_sgst_amount))
        
    def get_total_sgst_amount(self):
        self.__total_sgst_amount = self.__window.Element('_TOTAL_SGST_AMOUNT_').get()        
        return self.__total_sgst_amount

    def set_net_amount(self, total_net_amount):
        self.__net_amount = total_net_amount
        self.__window.Element('_NET_AMOUNT_').update(value = "{:.2f}".format(self.__net_amount))
        
    def get_net_amount(self):
        self.__net_amount = self.__window.Element('_NET_AMOUNT_').get()        
        return self.__net_amount

    def set_discount_amount(self, discount_amount):
        self.__discount_amount = discount_amount
        self.__window.Element('_DISCOUNT_AMOUNT_').update(value = "{:.2f}".format(self.__discount_amount))
        
    def get_discount_amount(self):
        self.__discount_amount = self.__window.Element('_DISCOUNT_AMOUNT_').get()        
        return self.__discount_amount

    def set_invoice_amount(self, invoice_amount):
        self.__invoice_amount = invoice_amount
        self.__window.Element('_INVOICE_AMOUNT_').update(value = "{:.2f}".format(self.__invoice_amount))
        
    def get_invoice_amount(self):
        self.__invoice_amount = self.__window.Element('_INVOICE_AMOUNT_').get()        
        return self.__invoice_amount

    def set_paid_amount(self, paid_amount):
        self.__paid_amount = paid_amount
        self.__window.Element('_PAID_AMOUNT_').update(value = "{:.2f}".format(self.__paid_amount))
        
    def get_paid_amount(self):
        self.__paid_amount = self.__window.Element('_paid_AMOUNT_').get()        
        return self.__paid_amount

    line_items = property(get_line_items, set_line_items)
    total_qty = property(get_total_qty, set_total_qty)
    total_amount = property(get_total_amount, set_total_amount)
    total_tax_amount = property(get_total_tax_amount, set_total_tax_amount)
    total_cgst_amount = property(get_total_cgst_amount, set_total_cgst_amount)
    total_sgst_amount = property(get_total_sgst_amount, set_total_sgst_amount)
    net_amount = property(get_net_amount, set_net_amount)
    discount_amount = property(get_discount_amount, set_discount_amount)
    invoice_amount = property(get_invoice_amount, set_invoice_amount)
    paid_amount = property(get_paid_amount, set_paid_amount)


class PaneKeypad:

    def __init__(self, window):
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
        window['UP'].Widget.config(takefocus=0)     
        window['DOWN'].Widget.config(takefocus=0)     
        window['LEFT'].Widget.config(takefocus=0)
        window['RIGHT'].Widget.config(takefocus=0)
        window['ENTER'].Widget.config(takefocus=0)
        window['BACKSPACE'].Widget.config(takefocus=0)
        window['FULL_STOP'].Widget.config(takefocus=0)
        window['TAB'].Widget.config(takefocus=0)


###
if __name__ == "__main__":
    print('***Not an executable module, please call python testClass.py')
