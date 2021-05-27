import PySimpleGUI as sg

"""
layout = [[sg.Text('AL FAREEDHA \n SUPER MARKET',size=(20,1))],
          [sg.Text('Try closing window with the "X"')],
          [sg.Button('Go'), sg.Button('Exit')]]
"""
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
                    ],pad=((20, 0), (50, 0),(50,0),(50,0)))
                ]
header= [
            sg.Column(
                [
                    [
                        sg.Image(filename='company-logo.GIF',pad=((30,0)))
                    ]
                ], size=(320, 90), vertical_alignment='center', justification='center',  pad=((0, 0), (0, 0),(0,0),(0,0)))
        ]

footer= [
            sg.Column(
                [
                    [
                        sg.Image(filename='valign-pos.gif', pad=((30, 0)))
                    ]
                ], size=(400, 90), vertical_alignment='center', justification='center', pad=((0, 0), (20, 0),(20,0),(20,0)))
        ]



layout = [
    [header],
    [sg.Text(' ', key='ErrMsg', size=(100, 1))],
    [sg.Text('User Name:', **txt_font,pad=((10, 5), (10, 0))),
     sg.In(key='-LOGINUSER-', pad=((0, 0), (15, 5)), size=(20, 1))],
    [sg.Text('Password:',**txt_font ,pad=((10, 5), (10, 0))),
     sg.In(key='-LOGINPWD-' ,password_char='*', pad=((0, 0), (15, 0)), size=(20, 1))],
    [sg.Text('Terminal:',**txt_font ,pad=((10, 5), (10, 0))),
     sg.In(key='-TERMINAL-', pad=((0, 0), (15, 5)), size=(20, 1), disabled=True)],
    [buttonLayout],
    [footer]
]

window = sg.Window('Login Window', layout, enable_close_attempted_event=True,no_titlebar=True,keep_on_top=True, size=(350, 450), return_keyboard_events=True,)

while True:
    event, values = window.read()
    print(event, values)
    if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit?') == 'Yes':
        break