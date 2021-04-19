import PySimpleGUI as sg
import sys
import platform

#sg.ChangeLookAndFeel('GreenTan')
sg.theme('SystemDefault')
#sg.set_options(element_padding=(0, 0))
theme_name_list = sg.theme_list()
#print(theme_name_list)
w, h = sg.Window.get_screen_size()

print(sys.version)
print(sys.version_info.major)
print(platform.python_version())
print(type(platform.python_version()))

column_heading=['Barcode','Item Name','Unit','Qty','MRP','Disc.','Price','Tax','Net']
reader = "100000 ItemName Kg 100 26 0 26 0 2600","100001 ItemName Kg 100 50 0 50 0 5000","100002 ItemName Kg 100 20 0 20 0 2600",\
        "100000 ItemName Kg 100 26 0 26 0 2600","100001 ItemName Kg 100 50 0 50 0 5000","100002 ItemName Kg 100 20 0 20 0 2600"
data1 = list(reader)

col_1_Layout = [
    [
        sg.Column(
        [
            [
                sg.Text('Invoice Entry', size=(15,1) ,font=("Helvetica", 20)),
                sg.Text('User:', font=("Helvetica", 12)),
                sg.Input(key='-USERID-',readonly=True, disabled_readonly_text_color='gray', disabled_readonly_background_color='gray89' ,default_text='admin' ,font=("Helvetica", 12),size=(15,1)),
                sg.Text('Terminal:',font=("Helvetica", 12)),
                sg.Input(key='-TERMINAL-', readonly=True ,disabled_readonly_text_color='gray', disabled_readonly_background_color='gray89', default_text='Terminal100' ,font=("Helvetica", 12),size=(15,1)),
                sg.Text('Date:',font=("Helvetica", 12)),
                sg.Input(key='-DATE-',readonly=True ,disabled_readonly_text_color='gray', disabled_readonly_background_color='gray89', default_text='16-apr-2021' ,font=("Helvetica", 12),size=(15,1)),
                sg.Text('UNPAID',font=("Helvetica", 15))        
            ]
        ], size = (985,50), vertical_alignment = 'top')    
    ],
    [
        sg.Column(
        [
            [
                sg.Text('Barcode:', size=(8,1),  font=("Helvetica", 12)),
                sg.Input(key='-BARCODE-NB-',background_color='White',font=("Helvetica", 12),size=(15,1)),
                sg.Text('Item Name:', size=(12,1), font=("Helvetica", 12)),
                sg.InputCombo(('Item Name','Item Name'),background_color='White',font=("Helvetica", 12),size=(40,1))            
            ]
        ], size = (985,50), vertical_alignment = 'top')    
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
        ], size = (985,410), vertical_alignment = 'top')    
    ],
    [
        sg.Column(
        [
            [
                sg.Button('F1\nChange Quantity', size=(14, 2), font='Helvetica 11 bold', key='F1'),
                sg.Button('F2\nChange Price', size=(14, 2), font='Helvetica 11 bold', key='F2'),
                sg.Button('F3\nCarry Bag', size=(14, 2), font='Helvetica 11 bold', key='F3')
            ],
            [
                sg.Button('F7\nLookup Customer', size=(14, 2), font='Helvetica 11 bold', key='F1'),
                sg.Button('F8\nDelete Invoice', size=(14, 2), font='Helvetica 11 bold', key='F2'),
                sg.Button('Esc\nExit', size=(14, 2), font='Helvetica 11 bold', key='ESC')
            ]               
        ], size = (985,125), vertical_alignment = 'top')    
    ]       
]

col_2_Layout = [
    [
        sg.Column(
        [
            [
                sg.Image(filename = 'company-logo.GIF')
            ]
        ], size = (220,90), vertical_alignment = 'top')    
    ],
    [
        sg.Column(
        [
            [
                sg.Text('Lines Items:',  font=("Helvetica", 11) , justification="right",size=(10,1)),
                sg.Input(key='-Lines-items-', readonly=True , disabled_readonly_text_color='gray', disabled_readonly_background_color='gray89', default_text='6' ,font=("Helvetica", 11), size=(12,1))          
            ],
            [
                sg.Text('Total Qty:',  font=("Helvetica", 11),justification="right",size=(10,1)),
                sg.Input(key='-Total-qty-', readonly=True , disabled_readonly_text_color='gray', disabled_readonly_background_color='gray89', default_text='600' ,font=("Helvetica", 11), size=(12,1))
            ],
            [
                sg.Text('MRP:',  font=("Helvetica", 11),justification="right",size=(10,1)),
                sg.Input(key='-mrp-', readonly=True,disabled_readonly_text_color='gray', disabled_readonly_background_color='gray89', default_text='2600' ,font=("Helvetica", 11),size=(12,1)),
            ],
            [
                sg.Text('Discounts:', font=("Helvetica", 11),justification="right",size=(10,1)),
                sg.Input(key='-Discounts-', readonly=True, disabled_readonly_text_color='gray', disabled_readonly_background_color='gray89', default_text='0.0' , font=("Helvetica", 11), size=(12,1)),
            ],
            [
                sg.Text('Price:', font=("Helvetica", 11),justification="right",size=(10,1)),
                sg.Input(key='-Price-', readonly=True, disabled_readonly_text_color='gray', disabled_readonly_background_color='gray89', default_text='2600.0' , font=("Helvetica", 11), size=(12,1)),
            ],
            [
                sg.Text('Tax:', font=("Helvetica", 11),justification="right",size=(10,1)),
                sg.Input(key='-tax-', readonly=True, disabled_readonly_text_color='gray', disabled_readonly_background_color='gray89', default_text='0.0' , font=("Helvetica", 11), size=(12,1)),
            ],
            [
                sg.Text('Net Amt:', font=("Helvetica", 11),justification="right",size=(10,1)),
                sg.Input(key='-Net-Amt-', readonly=True, disabled_readonly_text_color='gray', disabled_readonly_background_color='gray89', default_text='2600' ,font=("Helvetica", 11),size=(12,1)),
            ],
            [
                sg.Text('Paid Amt:', font=("Helvetica", 11),justification="right",size=(10,1)),
                sg.Input(key='-paid-amt-', readonly=True, disabled_readonly_text_color='gray', disabled_readonly_background_color='gray89', default_text='2600' , font=("Helvetica", 11), size=(12,1))
            ]            
            
        ], size = (220,263), vertical_alignment = 'top')    
    ],
    [
        sg.Column(
        [
            [
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T1', button_color = 'sky blue'),
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T2', button_color = 'sky blue'),
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T3', button_color = 'sky blue'),
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T3', button_color = 'sky blue'),                
                
            ],
            [
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T1', button_color = 'sky blue'),
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T2', button_color = 'sky blue'),
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T3', button_color = 'sky blue'),
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T3', button_color = 'sky blue'),                  
            ],
            [
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T1', button_color = 'sky blue'),
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T2', button_color = 'sky blue'),
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T3', button_color = 'sky blue'),
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T3', button_color = 'sky blue'),                
                
            ],
            [
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T1', button_color = 'sky blue'),
                sg.Button('1', size=(4, 2), font='Helvetica 11 bold', key='T2', button_color = 'sky blue'),
                sg.Button('1', size=(10, 2), font='Helvetica 11 bold', key='T3', button_color = 'sky blue'),
            ],            
        ], size = (220,218), vertical_alignment = 'top')    
    ],
    [
        sg.Column(
        [ 
        ], size = (220,63), vertical_alignment = 'top')    
    ]     
]

mainLayout = [
    [
        sg.Column(col_1_Layout, background_color = 'lightblue', size = (1000,665), vertical_alignment = 'top'),
        
        sg.Column(col_2_Layout, background_color = 'lightblue', size = (235,665), vertical_alignment = 'top'),        
    ]    
]

window = sg.Window('POS', mainLayout, location=(0,0), size=(w,h)
)

while True:
    event, values = window.read()
    print(event,values)
    if event == sg.WIN_CLOSED:
        break