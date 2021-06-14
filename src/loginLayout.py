import PySimpleGUI as sg

class loginLayout:

    btm_btn: dict = {'size': (10, 2), 'font': 'Helvetica 11 bold'}
    nvg_btn: dict = {'size': (40, 2), 'font': 'Helvetica 13 bold'}
    txt_font: dict = {'font': ('Helvetica 11 bold'), 'justification': 'right', 'size': (10, 1), 'text_color': 'black'}
    input_fld: dict = {'readonly': 'True', 'disabled_readonly_text_color': 'gray',
                       'disabled_readonly_background_color': 'gray89', 'size': (20, 1)}

    def header(self):
        return [
                [
                    sg.Image(filename='company-logo.GIF', pad=((0, 0)))
                ]
            ]


    def footer(self):
        return     [[
                            sg.Image(filename='valign-pos.GIF', pad=((0, 0)))
                        ]]
                    #vertical_alignment='center', justification='center',
                    #pad=((50, 0), (60, 0), (20, 0), (20, 0)))

    def loginButtons(self):
        return [
            [
                sg.Button('F12\nSign In', key='-LoginOk-', **self.btm_btn),
                sg.Button('Esc-Exit', key='Exit', **self.btm_btn)
            ]
        ]

    def login_body(self):
      return           \
              [
                [sg.Text(' ', key='ErrMsg', size=(100, 1))],
                [sg.Text('User Name:', **self.txt_font, pad=((20, 5), (10, 0))),
                 sg.In(key='-LOGINUSER-', focus=True, pad=((0, 0), (15, 5)), size=(20, 4))],
                [sg.Text('Password:', **self.txt_font, pad=((20, 5), (10, 0))),
                 sg.In(key='-LOGINPWD-', password_char='*', pad=((0, 0), (15, 0)), size=(20, 4))],
                [sg.Text('Terminal:', **self.txt_font, pad=((20, 5), (10, 0))),
                 sg.In(key='-TERMINAL-', **self.input_fld, pad=((0, 0), (15, 5)))]
                ]

    def login_page(self):
        return [
                    [
                        sg.Column(self.header(),size=(300,100), vertical_alignment='top', pad=((60, 0), (0, 0), (0, 0), (0, 0)))
                    ],
                    [
                        sg.Column(self.login_body(),size=(300,150), vertical_alignment='top',pad=((0, 0), (0, 0), (20, 0), (20, 0)) )
                    ],
                    [
                        sg.Column(self.loginButtons(),size=(300,100), vertical_alignment='top',pad=((60, 0), (30, 0), (20, 0), (20, 0)))
                    ],
                    [
                        sg.Column(self.footer(),size=(300,100), vertical_alignment='top',pad=((60, 0), (0, 0), (0, 0), (0, 0)))
                    ]
            ]


    def navigationMenu(self):
        return [
                    [
                        sg.Column(
                            [
                                [
                                    sg.Image(filename='company-logo.GIF', pad=((30, 0)))
                                ]
                            ], size=(320, 90), vertical_alignment='center', justification='center',
                            pad=((35, 0), (0, 0), (0, 0), (0, 0)))
                    ],
                    [
                        sg.Button('F1 - Estimate', key='-Estimate-', **self.nvg_btn, pad=((10, 10), (30, 0), (10, 0), (10, 0))),
                    ],
                    [
                        sg.Button('F2 - Invoice', key='-Invoice-', **self.nvg_btn, pad=((10, 10), (10, 0), (10, 0), (10, 0))),
                    ],
                    [
                        sg.Button('F3 - Cash', key='-Cash-', **self.nvg_btn, pad=((10, 10), (10, 0), (10, 0), (10, 0))),
                    ],
                    [
                        sg.Button('F4 - Settings', key='-Settings-', **self.nvg_btn, pad=((10, 10), (10, 0), (10, 0), (10, 0))),
                    ],
                    [
                        sg.Button('Esc - Sign Out', key='-SignOut-', **self.nvg_btn, pad=((10, 10), (10, 0), (10, 0), (10, 0))),
                    ],
                    [
                        sg.Column(
                            [
                                [
                                    sg.Image(filename='valign-pos.GIF', pad=((30, 0)))
                                ]
                            ], size=(400, 90), vertical_alignment='center', justification='center',
                            pad=((50, 0), (40, 0), (20, 0), (20, 0)))
                    ]
                ]
