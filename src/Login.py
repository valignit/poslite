import PySimpleGUI as sg
import json
import re
from DBOperations import DBOperations
from loginLayout import loginLayout
from InvoiceLayout import InvoiceLayout
from pynput.keyboard import Key, Controller


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

dbOperation = DBOperations(db_pos_host, db_pos_port, db_pos_name, db_pos_user, db_pos_passwd)
itemNames = dbOperation.fetchItemName()


heading: dict = {'size': (100, 1), 'font': ('Helvetica 20 bold'), 'text_color': 'blue'}
txt_font: dict = {'font': ('Helvetica 11 bold'), 'justification': 'right', 'size': (10, 1), 'text_color': 'black'}
input_fld: dict = {'readonly': 'True', 'disabled_readonly_text_color': 'gray',
                   'disabled_readonly_background_color': 'gray89', 'size': (20, 1)}

loginLayout = loginLayout()
invoiceLayout = InvoiceLayout()

header = loginLayout.header()
footer = loginLayout.footer()
#buttonLayout = loginLayout.loginButtons()
btm_btn: dict = {'size': (10, 2), 'font': 'Helvetica 11 bold'}
buttonLayout = [
                    sg.Column(
                    [
                        [
                            sg.Button('F12\nSign In', key='-LoginOk-', **btm_btn),
                            sg.Button('Esc-Exit', key='Exit', **btm_btn)
                        ]
                    ], pad=((50, 0), (50, 0), (50, 0), (50, 0)))
                ]


kb = Controller()
w, h = sg.Window.get_screen_size()
win_w = w
win_h = h
sg.theme('SystemDefault')

def open_popup_chg_qty(row_item, list_items, winObj,invfun):
    layout_chg_qty = invoiceLayout.layout_chg_qty(row_item,list_items)
    popup_chg_qty = sg.Window("Change Quantity", layout_chg_qty, location=(300, 250), size=(350, 180), modal=True,
                              finalize=True, return_keyboard_events=True, keep_on_top=True)
    popup_chg_qty.Element('-EXISTING-QTY-').update(value=str(list_items[row_item][4]))
    popup_chg_qty.Element('-NEW-QTY-').update(value='')

    while True:
        event, values = popup_chg_qty.read()
        print('eventc=', event)

        if event in ("Exit", '-CHG-QTY-ESC-', 'Escape:27') or event == sg.WIN_CLOSED:
            break
        if event == "-CHG-QTY-OK-" or event == "F12:123":
            event_chg_qty_ok_clicked( invoiceLayout, popup_chg_qty, row_item,winObj,invfun)
            break
    popup_chg_qty.close()


def event_chg_qty_ok_clicked(invoiceLayout , popup_chg_qty, row_item, winObj,invfun):
    applied_qty = 0
    existing_qty = popup_chg_qty.Element('-EXISTING-QTY-').get()
    applied_qty = popup_chg_qty.Element('-NEW-QTY-').get()
    if (applied_qty.isnumeric() or applied_qty.replace('.', '', 1).isdigit()):
        if float(applied_qty) == float(existing_qty):
            sg.popup('Quantity cannot be the same',keep_on_top = True)
            popup_chg_qty.Element('-NEW-QTY-').update(value='')
        else:
            tax_rate = invfun.list_items[row_item][7]
            selling_price = invfun.list_items[row_item][5]
            selling_amount = float(applied_qty) * float(selling_price)
            tax_amount = selling_amount * float(tax_rate) / 100
            net_price = selling_amount + tax_amount
            print('applied_qty:',applied_qty)
            invfun.list_items[row_item][4] = "{:.2f}".format(float(applied_qty))
            invfun.list_items[row_item][6] = "{:.2f}".format(selling_amount)
            invfun.list_items[row_item][8] = "{:.2f}".format(tax_amount)
            invfun.list_items[row_item][9] = "{:.2f}".format(net_price)
            print('after:',row_item,':',str(invfun.list_items))
            winObj.Element('-TABLE-').update(values=invfun.list_items, select_rows=[row_item])




def open_popup_payment(invfun,winObj):
    layout_payment = invoiceLayout.payment_layout()
    popup_payment = sg.Window("Payment", layout_payment, location=(300,250), size=(700,350), modal=True, finalize=True,return_keyboard_events=True, keep_on_top = True)

    invfun.initialize_payment_screen(popup_payment,winObj)

    prev_event = ''
    while True:
        event, values = popup_payment.read()
        print('eventc=', event)
        if event in ('\t', 'TAB') and prev_event == '-DISCOUNT-AMT-':
            invfun.event_discount_entered(popup_payment)

        if event in ('\t', 'TAB') and prev_event == '-MOBILE-NO-':
            invfun.event_mobile_number_entered(popup_payment)

        if event in ('\t', 'TAB') and prev_event == '-CASH-PAYMENT-':
            invfun.event_cash_card_payment_entered(popup_payment)

        if event in ('\t', 'TAB') and prev_event == '-CARD-PAYMENT-':
            invfun.event_cash_card_payment_entered(popup_payment)

        if event in ("Exit", '-PAYMENT-ESC-', 'Escape:27') or event == sg.WIN_CLOSED:
            break

        if event == "-PAYMENT-OK-" or event == "F12:123":
            invfun.event_payment_ok_clicked(popup_payment,winObj)
            break

        if event == "-PAID-" or event == "F12:123":
            invfun.event_paid_clicked(popup_payment)

        if event not in ('Up:38', 'Down:40', 'UP', 'DOWN', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            prev_event = event

    popup_payment.close()


def predict_text(searchItem, listItem):
    print('recied= ', searchItem, listItem)
    pattern = re.compile('.*' + searchItem + '.*')
    return [w for w in listItem if re.match(pattern, w)]


def searchItemWin(winObj):
    layout = InvoiceLayout.search_items_layout(itemNames,itemNames)
    window1 = sg.Window('Window Title', layout, keep_on_top=True, size=(400, 300), return_keyboard_events=True,
                        finalize=True)

    window1.bind('<Escape>', '')
    list_elem = window1.Element('_COMBO_')

    sel_item = 0
    while True:  # Event Loop
        event, values = window1.Read()
        if event is None or event == 'Exit' or event == 'Escape:27':
            # window.FindElement('-BARCODE-NB-')
            winObj.FindElement('-ITEMNAME-').Update('')
            winObj.FindElement('-BARCODE-NB-').Update('')
            window1.Close()
            break

        in_val = values['_INPUT_']
        if len(in_val) >= 2:
            prediction_list = predict_text(str(in_val), itemNames)
            list_elem.Update(values=prediction_list)
            if prediction_list:
                print('list fired', prediction_list[0])
                justName = str(prediction_list[0]).split('~')
                winObj.FindElement('-ITEMNAME-').Update(justName[0])
                winObj.FindElement('-BARCODE-NB-').Update(justName[1])
                list_elem.Widget.itemconfigure(0, bg='green', fg='white')
        else:
            list_elem.Update(values=itemNames)
        if event == '_COMBO_':
            print('Chose2', values['_COMBO_'])
            justName = str(values['_COMBO_']).split('~')
            winObj.FindElement('-ITEMNAME-').Update(justName[0])
            winObj.FindElement('-BARCODE-NB-').Update(justName[1])
        if event == 'Ok' or event == "F12:123":
            winObj.FindElement('-BARCODE-NB-').set_focus()
            window1.Close()
            break

    window1.Close()


def createInvoiceWin():
    # layoutMain = InvoiceLayout.layout_main

    col_1_Layout = InvoiceLayout.col1(self=InvoiceLayout)
    col_2_Layout = InvoiceLayout.col2(self=InvoiceLayout)

    layout_main = [
        [
            sg.Column(col_1_Layout, background_color='lightblue', vertical_alignment='top'),

            sg.Column(col_2_Layout, background_color='lightblue', vertical_alignment='top'),
        ]
    ]

    return sg.Window('POS', layout_main,
                     font='Helvetica 11', finalize=True, location=(0, 0), size=(win_w, win_h), keep_on_top=True,
                     resizable=True, return_keyboard_events=True, enable_close_attempted_event=True
                     )


def invoiceEntry():
    from InvoiceFunctions import InvoiceFunctions

    invfun = InvoiceFunctions()
    invWindow = createInvoiceWin()
    invWindow.force_focus()
    invWindow['-BARCODE-NB-'].set_focus()
    invWindow.Element('-STATUS-').update(value='UNPAID', text_color='Red')
    invWindow['-USERID-'].update(userid)
    invWindow['-TERMINAL-'].update(terminal)
    invWindow.bind('<Escape>', '')
    invWindow.Maximize()
    prev_event = ''
    focus_element = ''
    while True:
        event, values = invWindow.read()
        print('eventm=', event, '\nvalues=', values)
        if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == sg.WIN_CLOSED:
            if sg.popup_yes_no('Do you want to Exit?', title='Confirmation', keep_on_top=True) == 'Yes':
                navigateWin = 1
                break
        if event == 'Escape:27' or event == 'Exit':
            if sg.popup_yes_no('Do you want to Exit?', title='Confirmation', keep_on_top=True) == 'Yes':
                navigateWin = 1
                break
        if event == 'ESC':
            kb.press(Key.esc)
            kb.release(Key.esc)
        if event == 'TAB':
            kb.press(Key.tab)
            kb.release(Key.tab)
        if event == 'UP':
            kb.press(Key.up)
            kb.release(Key.up)
        if event == 'DOWN':
            kb.press(Key.down)
            kb.release(Key.down)
        if event == 'RIGHT':
            kb.press(Key.right)
            kb.release(Key.right)
        if event == 'LEFT':
            kb.press(Key.left)
            kb.release(Key.left)
        if event == 'BACK-SPACE':
            kb.press(Key.backspace)
            kb.release(Key.backspace)

        if event in ('T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9',
                     'T0') and window.FindElementWithFocus().Key == '-BARCODE-NB-':
            inp_val = window.Element('-BARCODE-NB-').get()
            inp_val += event[1]
            invWindow.Element('-BARCODE-NB-').update(value=inp_val)

        if event == 'FULL-STOP' and focus_element == '-BARCODE-NB-':
            inp_val = window.Element('-BARCODE-NB-').get()
            inp_val += '.'
            invWindow.Element('-BARCODE-NB-').update(value=inp_val)

        if event in ('\t', 'TAB') and prev_event == '-BARCODE-NB-':
            invoice_number = window.Element('-INVOICE_NO-').get()
            if invoice_number == '':
                invfun.proc_barcode(str(values['-BARCODE-NB-']), invWindow)

        if event in ('\t', 'TAB') and prev_event == '-ITEM_NAME-':
            invWindow['-TABLE-'].Widget.config(takefocus=1)
            if len(list_items) > 0:
                table_row = window['-TABLE-'].Widget.get_children()[0]
                invWindow['-TABLE-'].Widget.selection_set(table_row)  # move selection
                invWindow['-TABLE-'].Widget.focus(table_row)  # move focus
                invWindow['-TABLE-'].Widget.see(table_row)  # scroll to show i


        if event in ('F2:113', 'F2') and prev_event == '-TABLE-':
            invoice_number = invWindow.Element('-INVOICE_NO-').get()
            if invoice_number == '':
                sel_row = values['-TABLE-'][0]
                print('Selected ', sel_row)
                list_items = invWindow.Element('-TABLE-').get()
                print('Values ', list_items[sel_row])
                list_items.pop(sel_row)
                print('Length ', len(list_items))
                if len(list_items) > 0:
                    invWindow.Element('-TABLE-').update(values=list_items)
                    invWindow['-TABLE-'].Widget.selection_set(1)  # move selection
                    invWindow['-TABLE-'].Widget.focus(1)  # move focus
                    invWindow['-TABLE-'].Widget.see(1)  # scroll to show i
                if len(list_items) == 0:
                    invWindow.Element('-TABLE-').update(values=[])
                    invWindow.Element('-BARCODE-NB-').SetFocus()
                invfun.sum_item_list(invWindow)


        if event in ('F4:115', 'F4') and prev_event == '-TABLE-':
            invoice_number = invWindow.Element('-INVOICE_NO-').get()
            if invoice_number == '':
                sel_row = values['-TABLE-'][0]
                list_items = invWindow.Element('-TABLE-').get()
                print('initial:', str(list_items))
                open_popup_chg_qty(sel_row,list_items,invWindow,invfun)
                invWindow['-TABLE-'].Widget.config(takefocus=1)
                table_row = invWindow['-TABLE-'].Widget.get_children()[sel_row]
                invWindow['-TABLE-'].Widget.selection_set(table_row)  # move selection
                invWindow['-TABLE-'].Widget.focus(table_row)  # move focus
                invWindow['-TABLE-'].Widget.see(table_row)  # scroll to show i
                invfun.sum_item_list(invWindow)


        if event in ('F7:118', 'F7'):
            invfun.save_invoice(invWindow)
            invfun.clear_invoice(invWindow)
            invWindow.Element('-BARCODE-NB-').SetFocus()

        if event in ('F8:119', 'F8'):
            invoice_number = invWindow.Element('-INVOICE_NO-').get()
            if invoice_number == '':
                confirm_delete = sg.popup_ok_cancel('Invoice will be Deleted', keep_on_top=True)
                if confirm_delete == 'OK':
                    invfun.delete_invoice(invWindow)
                    invfun.clear_invoice(invWindow)
                    invWindow.Element('-BARCODE-NB-').SetFocus()

        if event in ('F12:123', 'F12'):
            invoice_number = invWindow.Element('-INVOICE_NO-').get()
            invoice_amt = invWindow.Element('-INVOICE-AMT-').get()
            if invoice_number == '' and float(invoice_amt) > 0:
                invfun.save_invoice(invWindow)
                open_popup_payment(invfun,invWindow)
                invWindow.Element('-BARCODE-NB-').SetFocus()

        if event in ('Home:36', 'BEGN'):
            invfun.save_invoice(invWindow)
            invfun.goto_first_invoice(invWindow)
            invWindow.Element('-BARCODE-NB-').SetFocus()


        if event in ('BEGN'):
            invfun.save_invoice(invWindow)
            invfun.goto_first_invoice(invWindow)
            invWindow.Element('-BARCODE-NB-').SetFocus()

        if event in ('Prior:33', 'PREV'):
            invfun.save_invoice(invWindow)
            invfun.goto_previous_invoice(invWindow)
            invWindow.Element('-BARCODE-NB-').SetFocus()

        if event in ('Next:33', 'NEXT'):
            invfun.save_invoice(invWindow)
            invfun.goto_next_invoice(invWindow)
            invWindow.Element('-BARCODE-NB-').SetFocus()

        if event in ('End:35', 'END'):
            invfun.save_invoice(invWindow)
            invfun.goto_last_invoice(invWindow)
            invWindow.Element('-BARCODE-NB-').SetFocus()

        if event in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0') and prev_event == '-BARCODE-NB-':
            invfun.proc_barcode(str(values['-BARCODE-NB-']),invWindow)

        if event not in ('Up:38', 'Down:40', 'UP', 'DOWN', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            prev_event = event

        if event == '-TABLE-':
            selected_row = values['-TABLE-'][0]
            print("select row ", selected_row)

        if event == "-SEARCH-ITME-" or event in ('F3:114', 'F3'):
            print('search item')
            searchItemWin(invWindow)
    if navigateWin == 1:
        invWindow.close()
        window['-LOGINUSER-'].update('')
        window['-LOGINPWD-'].update('')
        window.Element('-LOGINUSER-').set_focus()
        navigation()


def navigation():
    navigationMenu = loginLayout.navigationMenu()
    navigationWindow = sg.Window('Navigation Window', navigationMenu, enable_close_attempted_event=True,
                                 no_titlebar=True, modal=True, size=(350, 500), return_keyboard_events=True,
                                 finalize=True)

    navigationWindow.bind('<Escape>', exitPos())
    navigationWindow.bind('<F1>', '')
    navigationWindow.bind('<F2>', '')
    navigationWindow.bind('<F3>', '')
    navigationWindow.bind('<F4>', '')

    winFocus = 0
    while True:  # Event Loop
        event, values = navigationWindow.Read()
        print("navigation event", event)
        if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == sg.WIN_CLOSED:
            winFocus = 1
            break

        if event == '-SignOut-' or event == '<Escape>':
            if sg.popup_yes_no('Do you want to Exit?', title='Confirmation', keep_on_top=True) == 'Yes':
                navigationWindow.hide()
                winFocus = 1
                break
        if event == '-Invoice-' or event == 'F2:113':
            print('invoice screen')
            navigationWindow.close()
            invoiceEntry()

    if winFocus == 1:
        window.UnHide()
        window['-LOGINUSER-'].update('')
        window['-LOGINPWD-'].update('')
        window.force_focus()
        window.Element('-LOGINUSER-').SetFocus()
        print('login window open')

    navigationWindow.Close()


layout = [
    [header],
    [sg.Text(' ', key='ErrMsg', size=(100, 1))],
    [sg.Text('User Name:', **txt_font, pad=((20, 5), (10, 0))),
     sg.In(key='-LOGINUSER-', focus=True, pad=((0, 0), (15, 5)), size=(20, 4))],
    [sg.Text('Password:', **txt_font, pad=((20, 5), (10, 0))),
     sg.In(key='-LOGINPWD-', password_char='*', pad=((0, 0), (15, 0)), size=(20, 4))],
    [sg.Text('Terminal:', **txt_font, pad=((20, 5), (10, 0))),
     sg.In(key='-TERMINAL-', default_text=data['terminal_id'], **input_fld, pad=((0, 0), (15, 5)))],
    [
        sg.Column(
            [
                [
                    sg.Button('F12\nSign In', key='-LoginOk-', **btm_btn),
                    sg.Button('Esc-Exit', key='Exit', **btm_btn)
                ]
            ], pad=((50, 0), (50, 0), (50, 0), (50, 0)))
    ],
    [footer]
]

login_layout = loginLayout.login_page()



window = sg.Window('Login Window', login_layout, enable_close_attempted_event=True, no_titlebar=True, keep_on_top=True,
                   size=(350, 450), return_keyboard_events=True, finalize=True)

window.bind('<Escape>', exitPos())
window.bind('<F12>', login())
window.Element('-LOGINUSER-').set_focus()
window.Element('-TERMINAL-').update(data['terminal_id'])

userid = None
userpwd = None
terminal = None

while True:
    event, values = window.read()
    # print("main window = ", event, values)
    if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Exit') and sg.popup_yes_no('Do you really want to exit?',
                                                                                         title='Confirmation',
                                                                                         keep_on_top=True) == 'Yes':
        break
    if event == '<Escape>':
        if sg.popup_yes_no('Do you want to Exit?', title='Confirmation', keep_on_top=True) == 'Yes':
            break
    if event == '<F12>' or event == '-LoginOk-' or event == '<Enter>':
        userid  = window['-LOGINUSER-'].Get()
        userpwd = window['-LOGINPWD-'].Get()
        terminal = window['-TERMINAL-'].Get()
        print('login details', userid)
        db_item_row = dbOperation.verifyUser(userid, userpwd)
        if db_item_row is not None:
            print('Login successfull...')
            window.hide()
            navigation()
        else:
            print('Login Failed.....')
            window['ErrMsg'].update('Invalid Credential')
