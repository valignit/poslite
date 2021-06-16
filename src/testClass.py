import PySimpleGUI as sg
import datetime
import json
import sys
import platform
from pynput.keyboard import Key, Controller
from testClassUI import TestClassUI, PaneTitle, PaneHeader, PaneSearch, PaneDetail, PaneAction, PaneSummary, PaneKeypad


######
def initialize_title(pane):
    pane.user_id = 'XXX'
    pane.terminal_id = '101'
    pane.current_date = '01/01/2021'

def initialize_header(pane):
    pane.payment_status = 'UNPAID'
    pane.mobile_number = '0000000000'
    
def initialize_search(pane):
    pane.barcode = ''
    pane.item_name = ''
    pane.item_name = ''
    pane.focus_barcode()
    
def add_to_detail(pane):
    pane.item_code = 'ITEM-1001'
    pane.item_name = 'Hamam Soap'
    pane.uom = 'Nos'
    pane.qty = 1
    pane.selling_price = 35.00
    pane.cgst_tax_rate = 6.0
    pane.sgst_tax_rate = 6.0
    pane.selling_amount = pane.qty * pane.selling_price
    pane.tax_rate = pane.cgst_tax_rate + pane.sgst_tax_rate
    pane.tax_amount = pane.selling_amount * pane.tax_rate / 100
    pane.net_amount = pane.selling_amount + pane.tax_amount
    pane.add_line_item()


def process_barcode(barcode):
        sg.popup('processing barcode:',keep_on_top = True)



######
def main():
    with open('./alignpos.json') as file_config:
        config = json.load(file_config)

    kb = Controller()

    window = sg.Window('POS', TestClassUI.layout_main, background_color='White',
                       font='Helvetica 11', finalize=True, location=(0,0), size=(1600,800), keep_on_top=False, resizable=True,return_keyboard_events=True, use_default_focus=False
             )

    pane_title = PaneTitle(window)
    pane_header = PaneHeader(window)
    pane_search = PaneSearch(window)
    pane_detail = PaneDetail(window)
    pane_action = PaneAction(window)
    pane_summary = PaneSummary(window)
    pane_keypad = PaneKeypad(window)
    
    initialize_title(pane_title)
    initialize_header(pane_header)
    initialize_search(pane_search)

    prev_event = ''
      
    while True:
        event, values = window.read()
        print('eventm=', event)
        if event == sg.WIN_CLOSED:
            window.close()
            break
            
        if event == 'Escape:27':
            window.close()
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
            
        if event == 'BACKSPACE':
            kb.press(Key.backspace)
            kb.release(Key.backspace)  
            
        if event in ('F6:117', 'F6'):
            add_to_detail(pane_detail)
            
        if event in ('T1','T2','T3','T4','T5','T6','T7','T8','T9','T0') and window.FindElementWithFocus().Key == '_BARCODE_':
            inp_val = pane_search.barcode
            inp_val += event[1]
            pane_search.barcode = inp_val
            if len(pane_search.barcode) > 12:
                print('here0')            
                process_barcode(pane_search.barcode)
                
        if event in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0') and window.FindElementWithFocus().Key == '_BARCODE_':
            if len(pane_search.barcode) > 12:
                print('here1:', len(pane_search.barcode))
                process_barcode(pane_search.barcode)

        if event in ('\t', 'TAB') and prev_event == '_BARCODE_':
                print('here3')        
                process_barcode(pane_search.barcode)
        
        if event not in ('Up:38', 'Down:40', 'UP', 'DOWN', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            prev_event = event

    window.close()

######
if __name__ == "__main__":
    main()
