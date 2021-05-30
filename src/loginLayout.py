import PySimpleGUI as sg

class loginLayout:

    btm_btn: dict = {'size': (10, 2), 'font': 'Helvetica 11 bold'}
    nvg_btn: dict = {'size': (40, 2), 'font': 'Helvetica 13 bold'}

    def header(self):
        return [
                    sg.Column(
                    [
                        [
                            sg.Image(filename='company-logo.GIF', pad=((30, 0)))
                        ]
                    ], size=(320, 90), vertical_alignment='center', justification='center',
                    pad=((35, 0), (0, 0), (0, 0), (0, 0)))
                ]

    def footer(self):
        return [
                    sg.Column(
                    [
                        [
                            sg.Image(filename='valign-pos.GIF', pad=((30, 0)))
                        ]
                    ], size=(400, 90), vertical_alignment='center', justification='center',
                    pad=((50, 0), (60, 0), (20, 0), (20, 0)))
                ]

    def loginButtons(self):
        return [
                    sg.Column(
                    [
                        [
                            sg.Button('F12\nSign In', key='-LoginOk-', **self.btm_btn),
                            sg.Button('Esc-Exit', key='Exit', **self.btm_btn)
                        ]
                    ], pad=((50, 0), (50, 0), (50, 0), (50, 0)))
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
