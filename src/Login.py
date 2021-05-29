import PySimpleGUI as sg
import json
#import DBManager
#from DBManager import DBManager as dbManager
from DBOperations import DBOperations

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
btm_btn: dict = {'size':(10, 2), 'font':'Helvetica 11 bold'}
txt_font: dict = {'font':('Helvetica 11 bold'), 'justification':'right', 'size':(10, 1), 'text_color':'black'}

buttonLayout = [
                    sg.Column(
                    [
                        [
                            sg.Button('F12\nSign In', key='-LoginOk-', **btm_btn ),
                            sg.Button('Esc-Exit', key='Exit', **btm_btn)
                        ]
                    ],pad=((50, 0), (50, 0),(50,0),(50,0)))
                ]
header= [
            sg.Column(
                [
                    [
                        sg.Image(filename='company-logo.GIF',pad=((30,0)))
                    ]
                ], size=(320, 90), vertical_alignment='center', justification='center',  pad=((35, 0), (0, 0),(0,0),(0,0)))
        ]

footer= [
            sg.Column(
                [
                    [
                        sg.Image(filename='valign-pos.GIF', pad=((30, 0)))
                    ]
                ], size=(400, 90), vertical_alignment='center', justification='center', pad=((50, 0), (60, 0),(20,0),(20,0)))
        ]

input_fld: dict = {'readonly':'True', 'disabled_readonly_text_color':'gray','disabled_readonly_background_color':'gray89','size':(20, 1)}

layout = [
    [header],
    [sg.Text(' ', key='ErrMsg', size=(100, 1))],
    [sg.Text('User Name:', **txt_font,pad=((20, 5), (10, 0))),
     sg.In(key='-LOGINUSER-', pad=((0, 0), (15, 5)), size=(20, 1))],
    [sg.Text('Password:',**txt_font ,pad=((20, 5), (10, 0))),
     sg.In(key='-LOGINPWD-' ,password_char='*', pad=((0, 0), (15, 0)), size=(20, 1))],
    [sg.Text('Terminal:',**txt_font ,pad=((20, 5), (10, 0))),
     sg.In(key='-TERMINAL-', default_text=data['terminal_id'],**input_fld , pad=((0, 0), (15, 5)))],
    [buttonLayout],
    [footer]
]

window = sg.Window('Login Window', layout, enable_close_attempted_event=True,no_titlebar=True,keep_on_top=True, size=(350, 450), return_keyboard_events=True,finalize=True)

window.bind('<Escape>', exitPos())
window.bind('<F12>', login())

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
            break
        else:
            print('Login Failed.....')
            window['ErrMsg'].update('Invalid Credential')