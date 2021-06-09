import PySimpleGUI as sg
import mariadb
import datetime
import json
import sys
import os

from pynput.keyboard import Key, Controller
from DBOperations import DBOperations
from DBManager import DBManager


class InvoiceFunctions:


    with open('./alignpos.json') as file_config:
        data = json.load(file_config)

    db_pos_host = data['db_pos_host']
    db_pos_port = data['db_pos_port']
    db_pos_name = data['db_pos_name']
    db_pos_user = data['db_pos_user']
    db_pos_passwd = data['db_pos_passwd']
    ws_erp_user = data["ws_erp_user"]

    dbOperation = DBOperations(db_pos_host, db_pos_port, db_pos_name, db_pos_user, db_pos_passwd)
    db = DBManager()

    kb = Controller()
    list_items = []
    now = datetime.datetime.now()

    def isInteger(self,inp):
        try:
            val = int(inp)
            return True
        except ValueError:
            return False

    def isFloat(self,inp):
        try:
            val = float(inp)
            return True
        except ValueError:
            return False




    def proc_barcode(self,barcode, window):

        if not len(barcode) == 13:
            return

        if not self.isInteger(barcode):
            window.Element('-BARCODE-NB-').update(value='')
            window.Element('-BARCODE-NB-').set_focus()
            return

        db_pos_sql_stmt = "SELECT item_code, item_name, uom, selling_price, cgst_tax_rate, sgst_tax_rate from tabItem where barcode = %s"
        db_pos_sql_data = (barcode,)
        db_item_row = None
        try:
            db_item_row = self.db.query_with_param(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error - 001: {db_err}")
            #db_pos_conn.close()
            sys.exit(1)

        if db_item_row is None:
            sg.popup('Item not found', keep_on_top=True)
            window.Element('-BARCODE-NB-').update(value='')
            window.Element('-BARCODE-NB-').set_focus()
            return

        item_code = db_item_row[0]
        item_name = db_item_row[1]
        uom = db_item_row[2]
        qty = 1
        selling_price = db_item_row[3]
        cgst_tax_rate = db_item_row[4]
        sgst_tax_rate = db_item_row[5]
        row_item = []
        row_item.append(item_code)
        row_item.append(barcode)
        row_item.append(item_name)
        row_item.append(uom)
        row_item.append("{:.2f}".format(qty))
        row_item.append("{:.2f}".format(selling_price))
        selling_amount = float(qty) * float(selling_price)
        row_item.append("{:.2f}".format(selling_amount))
        tax_rate = float(cgst_tax_rate) + float(sgst_tax_rate)
        row_item.append(tax_rate)
        tax_amount = selling_amount * tax_rate / 100
        row_item.append("{:.2f}".format(tax_amount))
        net_price = selling_amount + tax_amount
        row_item.append("{:.2f}".format(net_price))
        row_item.append(cgst_tax_rate)
        row_item.append(sgst_tax_rate)
        self.list_items.append(row_item)
        window.Element('-TABLE-').update(values=self.list_items)
        window.Element('-BARCODE-NB-').update(value='')
        window.Element('-ITEMNAME-').update(value='')
        window.Element('-BARCODE-NB-').set_focus()
        self.sum_item_list(window)


    def sum_item_list(self,winObj):
        line_items = 0
        total_qty = 0.0
        total_price = 0.0
        total_tax = 0.0
        total_net_price = 0.0

        for row_item in self.list_items:
            line_items += 1
            total_qty += float(row_item[4])
            total_price += float(row_item[6])
            total_tax += float(row_item[8])
            total_net_price += float(row_item[9])

        winObj.Element('-LINE-ITEMS-').update(value=str(line_items))
        winObj.Element('-TOTAL-QTY-').update(value="{:.2f}".format(total_qty))
        winObj.Element('-TOTAL-PRICE-').update(value="{:.2f}".format(total_price))
        winObj.Element('-TOTAL-TAX-').update(value="{:.2f}".format(total_tax))
        winObj.Element('-NET-PRICE-').update(value="{:.2f}".format(total_net_price))
        winObj.Element('-INVOICE-AMT-').update(value="{:.2f}".format(total_net_price))


    ######
    # Save the Invoice to DB
    def save_invoice(self,winObj):

        invoice_number = winObj.Element('-INVOICE_NO-').get()
        if invoice_number != '':
            return

        reference_number = winObj.Element('-REFERENCE_NO-').get()
        if reference_number == '' and len(self.list_items) > 0:
            self.insert_invoice(winObj)


    def insert_invoice(self,winObj):
        print('insert')
        reference_number = ''
        if len(self.list_items) == 0:
            return
        db_pos_sql_stmt = "SELECT nextval('REFERENCE_NUMBER')"
        try:
            db_item_row = self.db.query_one(db_pos_sql_stmt)
            #db_pos_cur.execute(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error - 002: {db_err}")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            self.db.close()
            sys.exit(1)
        print('ref no')

        #db_item_row = self.db.fetchone()
        if db_item_row is None:
            print('Sequence not found')
        else:
            reference_number = db_item_row[0]
        print(reference_number , db_item_row[0])
        total_amount = winObj.Element('-TOTAL-PRICE-').get()
        net_amount = winObj.Element('-NET-PRICE-').get()
        invoice_amount = winObj.Element('-INVOICE-AMT-').get()
        cgst_tax_amount = 0.0 #winObj.Element('-TOTAL-CGST-').get()
        sgst_tax_amount = 0.0 #winObj.Element('-TOTAL-SGST-').get()
        terminal_id = winObj.Element('-TERMINAL-').get()
        db_pos_sql_stmt = (
            "INSERT INTO tabInvoice (name, posting_date, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, terminal_id, creation, owner)"
            "VALUES (%s, now(), %s, %s, %s, %s, %s, %s, now(), %s)")
        db_pos_sql_data = (
        reference_number, '0000000000', total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, terminal_id,self.ws_erp_user)
        try:
            self.db.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error - 003: {db_err}")
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            #self.db.rollback()
            #self.db.close()
            sys.exit(1)

        item_count = 0
        print('complete list', self.list_items)
        for row_item in self.list_items:
            item_count += 1
            item_code = row_item[0]
            qty = row_item[4]
            selling_price = row_item[6]
            cgst_tax_rate = 0.0 #row_item[10]
            sgst_tax_rate = 0.0 #row_item[11]
            name = reference_number + f"{item_count:04d}"
            print(name)
            print('InvoiceItem:', name, ':', item_code)

            db_pos_sql_stmt = (
                "INSERT INTO `tabInvoice Item` (name, parent, item_code, qty, standard_selling_price, applied_selling_price, cgst_tax_rate, sgst_tax_rate)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            db_pos_sql_data = (
            name, reference_number, item_code, qty, selling_price, selling_price, cgst_tax_rate, sgst_tax_rate)

            #db_pos_sql_stmt = "INSERT INTO `tabInvoice Item` (name, parent, item_code, qty, standard_selling_price, applied_selling_price, cgst_tax_rate, sgst_tax_rate) VALUES ('0004', '1111', 'ITEM-1002', 1, 10, 10, 0.0, 0.0)"

            try:
                self.db.execute(db_pos_sql_stmt, db_pos_sql_data)
                self.db.commit()
            except mariadb.Error as db_err:
                print(f"POS database error - 004: {db_err}")
                #self.db.rollback()
                #self.db.close()
                sys.exit(1)
        self.db.commit()


    def clear_invoice(self,window):
        print('clear')

        line_items = 0
        total_qty = 0
        total_price = 0
        total_tax = 0
        total_net_price = 0
        discount_amt = 0
        total_cgst = 0
        total_sgst = 0
        total_payment = 0
        self.list_items.clear()
        row_item = []
        window.Element('-LINE-ITEMS-').update(value=str(line_items))
        window.Element('-TOTAL-QTY-').update(value="{:.2f}".format(total_qty))
        window.Element('-TOTAL-PRICE-').update(value="{:.2f}".format(total_price))
        window.Element('-TOTAL-TAX-').update(value="{:.2f}".format(total_tax))
        window.Element('-NET-PRICE-').update(value="{:.2f}".format(total_net_price))
        window.Element('-INVOICE-AMT-').update(value="{:.2f}".format(total_net_price))
        window.Element('-TOTAL-CGST-').update(value="{:.2f}".format(total_cgst))
        window.Element('-TOTAL-SGST-').update(value="{:.2f}".format(total_sgst))
        window.Element('-DISCOUNT-').update(value="{:.2f}".format(discount_amt))
        window.Element('-PAID-AMT-').update(value="{:.2f}".format(total_payment))
        window.Element('-TABLE-').update(values=self.list_items)
        window.Element('-INVOICE_NO-').update(value='')
        window.Element('-REFERENCE_NO-').update(value='')
        window.Element('-MOBILE_NO-').update(value='')


    def update_invoice(self,window):
        print('update')
        mobile_number = window.Element('-MOBILE_NO-').get()
        total_amount = window.Element('-TOTAL-PRICE-').get()
        invoice_amount = window.Element('-INVOICE-AMT-').get()
        cgst_tax_amount = window.Element('-TOTAL-CGST-').get()
        sgst_tax_amount = window.Element('-TOTAL-SGST-').get()
        terminal_id = window.Element('-TERMINAL-').get()
        reference_number = window.Element('-REFERENCE_NO-').get()

        db_pos_sql_stmt = (
            "UPDATE tabInvoice SET posting_date=now(), customer=%s, total_amount=%s, cgst_tax_amount=%s, sgst_tax_amount=%s, invoice_amount=%s, terminal_id=%s, creation=now(), owner=%s"
            " WHERE name = %s")
        db_pos_sql_data = (
        mobile_number, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, terminal_id, self.ws_erp_user,
        reference_number)
        try:
            self.db.execute(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error - 005: {db_err}")
            #db_pos_conn.rollback()
            #db_pos_conn.close()
            sys.exit(1)
        print('here1', reference_number)
        db_pos_sql_stmt = ("DELETE FROM `tabInvoice Item` WHERE parent = '" + reference_number + "'")

        try:
            self.db.execute(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error - 006: {db_err}")
            #db_pos_conn.rollback()
            #db_pos_conn.close()
            sys.exit(1)
        print('here2')

        item_count = 0
        for row_item in self.list_items:
            item_count += 1
            item_code = row_item[0]
            qty = row_item[4]
            selling_price = row_item[6]
            cgst_tax_rate = row_item[10]
            sgst_tax_rate = row_item[11]
            name = reference_number + f"{item_count:04d}"
            print(name)

            db_pos_sql_stmt = (
                "INSERT INTO `tabInvoice Item` (name, parent, item_code, qty, standard_selling_price, applied_selling_price, cgst_tax_rate, sgst_tax_rate)"
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            db_pos_sql_data = (
            name, reference_number, item_code, qty, selling_price, selling_price, cgst_tax_rate, sgst_tax_rate)
            try:
                self.db.execute(db_pos_sql_stmt, db_pos_sql_data)
            except mariadb.Error as db_err:
                print(f"POS database error - 007: {db_err}")
                #db_pos_conn.rollback()
                #db_pos_conn.close()
                sys.exit(1)
        self.db.commit()

    def delete_invoice(self,window):
        print('delete')
        reference_number = window.Element('-REFERENCE_NO-').get()
        if reference_number == '':
            return
        db_pos_sql_stmt = ("DELETE FROM `tabInvoice Item` WHERE parent = '" + reference_number + "'")
        print(db_pos_sql_stmt)
        try:
            self.db.execute(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error - 008: {db_err}")
            #db_pos_conn.rollback()
            #db_pos_conn.close()
            sys.exit(1)

        db_pos_sql_stmt = ("DELETE FROM `tabInvoice` WHERE name = '" + reference_number + "'")
        try:
            self.db.execute(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error - 009: {db_err}")
            #db_pos_conn.rollback()
            #db_pos_conn.close()
            sys.exit(1)
        self.db.commit()


    def goto_previous_invoice(self,window):
        print('prev')
        reference_number = window.Element('-REFERENCE_NO-').get()
        if (reference_number == ''):
            db_pos_sql_stmt = (
                "SELECT name, invoice_number, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, discount_amount, paid_amount from tabInvoice WHERE name = (select max(name) from tabInvoice)")
            try:
                self.db.execute(db_pos_sql_stmt)
            except mariadb.Error as db_err:
                print(f"POS database error - 010: {db_err}")
                #db_pos_conn.close()
                sys.exit(1)
        else:
            db_pos_sql_stmt = (
                "SELECT name, invoice_number, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, discount_amount, paid_amount from tabInvoice WHERE name = (select max(name) from tabInvoice where name < %s)")
            db_pos_sql_data = (reference_number,)

            try:
                self.db.execute(db_pos_sql_stmt, db_pos_sql_data)
            except mariadb.Error as db_err:
                print(f"POS database error - 011: {db_err}")
                #db_pos_conn.close()
                sys.exit(1)

        db_invoice_row = self.db.fetchone()
        if db_invoice_row is None:
            print('Invoice not found')
        else:
            window.Element('-REFERENCE_NO-').update(value='')
            window.Element('-INVOICE_NO-').update(value='')
            window.Element('-MOBILE_NO-').update(value='')
            window.Element('-STATUS-').update(value='UNPAID', text_color='Red')
            reference_number = db_invoice_row[0]
            window.Element('-REFERENCE_NO-').update(value=reference_number)
            invoice_number = db_invoice_row[1]
            window.Element('-INVOICE_NO-').update(value=invoice_number)
            mobile_number = db_invoice_row[2]

            retval = db_invoice_row[6]
            retval = '0.00' if retval == '' or not retval else retval
            invoice_amount = float(retval)

            retval = db_invoice_row[7]
            retval = '0.00' if retval == '' or not retval else retval
            discount_amount = float(retval)

            retval = db_invoice_row[8]
            retval = '0.00' if retval == '' or not retval else retval
            paid_amount = float(retval)

            window.Element('-MOBILE_NO-').update(value=mobile_number)

            if invoice_number:
                window.Element('-STATUS-').update(value='PAID', text_color='Lime Green')
            else:
                window.Element('-STATUS-').update(value='UNPAID', text_color='Red')
            window.Element('-DISCOUNT-').update(value="{:.2f}".format(discount_amount))
            window.Element('-INVOICE-AMT-').update(value="{:.2f}".format(invoice_amount))
            window.Element('-PAID-AMT-').update(value="{:.2f}".format(paid_amount))


            db_pos_sql_stmt = (
                "SELECT inv_item.item_code, item_name, barcode, uom, qty,standard_selling_price, applied_selling_price, inv_item.cgst_tax_rate,inv_item.sgst_tax_rate from `tabInvoice Item` inv_item, tabItem item WHERE inv_item.parent = %s and inv_item.item_code = item.item_code")
            db_pos_sql_data = (reference_number,)
            print(db_pos_sql_stmt)
            try:
                self.db.execute(db_pos_sql_stmt, db_pos_sql_data)
            except mariadb.Error as db_err:
                print(f"POS database error - 012: {db_err}")
                #db_pos_conn.close()
                sys.exit(1)
            print('here2 ', db_invoice_row[0])

            db_items = self.db.fetchall()
            row_item = []
            self.list_items.clear()

            for db_item_row in db_items:
                item_code = db_item_row[0]
                item_name = db_item_row[1]
                barcode = db_item_row[2]
                uom = db_item_row[3]
                qty = db_item_row[4]
                selling_price = db_item_row[5]
                cgst_tax_rate = db_item_row[7]
                sgst_tax_rate = db_item_row[8]
                selling_amount = float(qty) * float(selling_price)
                tax_rate = float(cgst_tax_rate) + float(sgst_tax_rate)
                tax_amount = selling_amount * tax_rate / 100
                net_amount = selling_amount + tax_amount
                row_item.append(item_code)
                row_item.append(barcode)
                row_item.append(item_name)
                row_item.append(uom)
                row_item.append("{:.2f}".format(qty))
                row_item.append("{:.2f}".format(selling_price))
                row_item.append("{:.2f}".format(selling_amount))
                row_item.append("{:.2f}".format(tax_rate))
                row_item.append("{:.2f}".format(tax_amount))
                row_item.append("{:.2f}".format(net_amount))
                row_item.append("{:.2f}".format(cgst_tax_rate))
                row_item.append("{:.2f}".format(sgst_tax_rate))
                self.list_items.append(row_item)
            window.Element('-TABLE-').update(values=self.list_items)
            print('\nlist_items:', self.list_items)
            self.sum_item_list(window)


    def goto_next_invoice(self,window):
        print('next')
        reference_number = window.Element('-REFERENCE_NO-').get()
        if (reference_number == ''):
            return
        else:
            db_pos_sql_stmt = (
                "SELECT name, invoice_number, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, discount_amount, paid_amount from tabInvoice WHERE name = (select min(name) from tabInvoice where name > %s)")
            db_pos_sql_data = (reference_number,)

            try:
                db_invoice_row = self.db.query_one(db_pos_sql_stmt, db_pos_sql_data)
            except mariadb.Error as db_err:
                print(f"POS database error - 013: {db_err}")
                #db_pos_conn.close()
                sys.exit(1)

        #db_invoice_row = db_pos_cur.fetchone()
        if db_invoice_row is None:
            print('Invoice not found')
        else:
            window.Element('-REFERENCE_NO-').update(value='')
            window.Element('-INVOICE_NO-').update(value='')
            window.Element('-MOBILE_NO-').update(value='')
            window.Element('-STATUS-').update(value='UNPAID', text_color='Red')
            reference_number = db_invoice_row[0]
            window.Element('-REFERENCE_NO-').update(value=reference_number)
            invoice_number = db_invoice_row[1]
            window.Element('-INVOICE_NO-').update(value=invoice_number)
            mobile_number = db_invoice_row[2]

            retval = db_invoice_row[6]
            retval = '0.00' if retval == '' or not retval else retval
            invoice_amount = float(retval)

            retval = db_invoice_row[7]
            retval = '0.00' if retval == '' or not retval else retval
            discount_amount = float(retval)

            retval = db_invoice_row[8]
            retval = '0.00' if retval == '' or not retval else retval
            paid_amount = float(retval)

            window.Element('-MOBILE_NO-').update(value=mobile_number)
            if invoice_number:
                window.Element('-STATUS-').update(value='PAID', text_color='Lime Green')
            else:
                window.Element('-STATUS-').update(value='UNPAID', text_color='Red')
            window.Element('-DISCOUNT-').update(value="{:.2f}".format(discount_amount))
            window.Element('-INVOICE-AMT-').update(value="{:.2f}".format(invoice_amount))
            window.Element('-PAID-AMT-').update(value="{:.2f}".format(paid_amount))

            db_pos_sql_stmt = (
                "SELECT inv_item.item_code, item_name, barcode, uom, qty,standard_selling_price, applied_selling_price, inv_item.cgst_tax_rate,inv_item.sgst_tax_rate from `tabInvoice Item` inv_item, tabItem item WHERE inv_item.parent = %s and inv_item.item_code = item.item_code")
            db_pos_sql_data = (reference_number,)
            print(db_pos_sql_stmt)
            try:
                db_items = self.db.query(db_pos_sql_stmt, db_pos_sql_data)
            except mariadb.Error as db_err:
                print(f"POS database error - 014: {db_err}")
                #db_pos_conn.close()
                sys.exit(1)

            #db_items = db_pos_cur.fetchall()
            row_item = []
            self.list_items.clear()

            for db_item_row in db_items:
                item_code = db_item_row[0]
                item_name = db_item_row[1]
                barcode = db_item_row[2]
                uom = db_item_row[3]
                qty = db_item_row[4]
                selling_price = db_item_row[5]
                print('price:', selling_price, ' ', db_item_row[5])

                cgst_tax_rate = db_item_row[7]
                sgst_tax_rate = db_item_row[8]
                selling_amount = float(qty) * float(selling_price)
                tax_rate = float(cgst_tax_rate) + float(sgst_tax_rate)
                tax_amount = selling_amount * tax_rate / 100
                net_amount = selling_amount + tax_amount
                row_item = []
                row_item.append(item_code)
                row_item.append(barcode)
                row_item.append(item_name)
                row_item.append(uom)
                row_item.append("{:.2f}".format(qty))
                row_item.append("{:.2f}".format(selling_price))
                row_item.append("{:.2f}".format(selling_amount))
                row_item.append("{:.2f}".format(tax_rate))
                row_item.append("{:.2f}".format(tax_amount))
                row_item.append("{:.2f}".format(net_amount))
                row_item.append("{:.2f}".format(cgst_tax_rate))
                row_item.append("{:.2f}".format(sgst_tax_rate))
                self.list_items.append(row_item)
                window.Element('-TABLE-').update(values=self.list_items)
            self.sum_item_list(window)

    def goto_last_invoice(self,window):
        print('last')
        db_pos_sql_stmt = (
            "SELECT name, invoice_number, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount from tabInvoice WHERE name = (select max(name) from tabInvoice)")

        try:
            self.db.execute(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error - 016: {db_err}")
            #db_pos_conn.close()
            sys.exit(1)

        db_invoice_row = self.db.fetchone()
        if db_invoice_row is None:
            print('Invoice not found')
        else:
            print('here1 ', db_invoice_row[0])
            reference_number = db_invoice_row[0]
            window.Element('-REFERENCE_NO-').update(value=reference_number)
            mobile_number = db_invoice_row[2]
            window.Element('-MOBILE_NO-').update(value=mobile_number)
            db_pos_sql_stmt = (
                "SELECT inv_item.item_code, item_name, barcode, uom, qty,standard_selling_price, applied_selling_price, inv_item.cgst_tax_rate,inv_item.sgst_tax_rate from `tabInvoice Item` inv_item, tabItem item WHERE inv_item.parent = %s and inv_item.item_code = item.item_code")
            db_pos_sql_data = (reference_number,)
            print(db_pos_sql_stmt)
            try:
                self.db.execute(db_pos_sql_stmt, db_pos_sql_data)
            except mariadb.Error as db_err:
                print(f"POS database error - 017: {db_err}")
                #db_pos_conn.close()
                sys.exit(1)
            print('here2 ', db_invoice_row[0])

            db_items = self.db.fetchall()
            row_item = []
            self.list_items.clear()

            for db_item_row in db_items:
                item_code = db_item_row[0]
                item_name = db_item_row[1]
                barcode = db_item_row[2]
                uom = db_item_row[3]
                qty = db_item_row[4]
                selling_price = db_item_row[5]
                cgst_tax_rate = db_item_row[7]
                sgst_tax_rate = db_item_row[8]
                selling_amount = float(qty) * float(selling_price)
                tax_rate = float(cgst_tax_rate) + float(sgst_tax_rate)
                print(tax_rate, cgst_tax_rate, sgst_tax_rate)
                tax_amount = selling_amount * tax_rate / 100
                net_amount = selling_amount + tax_amount
                row_item.append(item_code)
                row_item.append(barcode)
                row_item.append(item_name)
                row_item.append(uom)
                row_item.append(qty)
                row_item.append("{:.2f}".format(selling_price))
                row_item.append("{:.2f}".format(selling_amount))
                row_item.append("{:.2f}".format(tax_rate))
                row_item.append("{:.2f}".format(tax_amount))
                row_item.append("{:.2f}".format(net_amount))
                row_item.append("{:.2f}".format(cgst_tax_rate))
                row_item.append("{:.2f}".format(sgst_tax_rate))
                self.list_items.append(row_item)
                window.Element('-TABLE-').update(values=self.list_items)
            self.sum_item_list(window)


    def goto_first_invoice(self,window):
        print('first')
        db_pos_sql_stmt = (
            "SELECT name, invoice_number, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount from tabInvoice WHERE name = (select min(name) from tabInvoice)")

        try:
            self.db.execute(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error - 018: {db_err}")
            #db_pos_conn.close()
            sys.exit(1)

        db_invoice_row = self.db.fetchone()
        if db_invoice_row is None:
            print('Invoice not found')
        else:
            print('here1 ', db_invoice_row[0])
            reference_number = db_invoice_row[0]
            window.Element('-REFERENCE_NO-').update(value=reference_number)
            mobile_number = db_invoice_row[2]
            window.Element('-MOBILE_NO-').update(value=mobile_number)
            db_pos_sql_stmt = (
                "SELECT inv_item.item_code, item_name, barcode, uom, qty,standard_selling_price, applied_selling_price, inv_item.cgst_tax_rate, inv_item.sgst_tax_rate from `tabInvoice Item` inv_item, tabItem item WHERE inv_item.parent = %s and inv_item.item_code = item.item_code")
            db_pos_sql_data = (reference_number,)
            print(db_pos_sql_stmt)
            try:
                self.db.execute(db_pos_sql_stmt, db_pos_sql_data)
            except mariadb.Error as db_err:
                print(f"POS database error - 019: {db_err}")
                #db_pos_conn.close()
                sys.exit(1)
            print('here2 ', db_invoice_row[0])

            db_items = self.db.fetchall()
            row_item = []
            self.list_items.clear()

            for db_item_row in db_items:
                item_code = db_item_row[0]
                item_name = db_item_row[1]
                barcode = db_item_row[2]
                uom = db_item_row[3]
                qty = db_item_row[4]
                selling_price = db_item_row[5]
                cgst_tax_rate = db_item_row[7]
                sgst_tax_rate = db_item_row[8]
                selling_amount = float(qty) * float(selling_price)
                tax_rate = float(cgst_tax_rate) + float(sgst_tax_rate)
                tax_amount = selling_amount * tax_rate / 100
                net_amount = selling_amount + tax_amount
                row_item.append(item_code)
                row_item.append(barcode)
                row_item.append(item_name)
                row_item.append(uom)
                row_item.append(qty)
                row_item.append("{:.2f}".format(selling_price))
                row_item.append("{:.2f}".format(selling_amount))
                row_item.append("{:.2f}".format(tax_rate))
                row_item.append("{:.2f}".format(tax_amount))
                row_item.append("{:.2f}".format(net_amount))
                row_item.append("{:.2f}".format(cgst_tax_rate))
                row_item.append("{:.2f}".format(sgst_tax_rate))
                self.list_items.append(row_item)
                window.Element('-TABLE-').update(values=self.list_items)
            self.sum_item_list(window)

    def goto_first_invoice(self, window):
        print('first')
        db_pos_sql_stmt = (
            "SELECT name, invoice_number, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount, discount_amount, paid_amount from tabInvoice WHERE name = (select min(name) from tabInvoice)")

        try:
            db_invoice_row = self.db.query_one(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error - 017: {db_err}")
            #db_pos_conn.close()
            sys.exit(1)

        #db_invoice_row = db_pos_cur.fetchone()
        if db_invoice_row is None:
            print('Invoice not found')
        else:
            window.Element('-REFERENCE_NO-').update(value='')
            window.Element('-INVOICE_NO-').update(value='')
            window.Element('-MOBILE_NO-').update(value='')

            reference_number = db_invoice_row[0]
            invoice_number = db_invoice_row[1]
            mobile_number = db_invoice_row[2]

            retval = db_invoice_row[6]
            retval = '0.00' if retval == '' or not retval else retval
            invoice_amount = float(retval)

            retval = db_invoice_row[7]
            retval = '0.00' if retval == '' or not retval else retval
            discount_amount = float(retval)

            retval = db_invoice_row[8]
            retval = '0.00' if retval == '' or not retval else retval
            paid_amount = float(retval)

            window.Element('-REFERENCE_NO-').update(value=reference_number)
            window.Element('-INVOICE_NO-').update(value=invoice_number)
            window.Element('-MOBILE_NO-').update(value=mobile_number)
            if invoice_number:
                window.Element('-STATUS-').update(value='PAID', text_color='Lime Green')
            else:
                window.Element('-STATUS-').update(value='UNPAID', text_color='Red')
            window.Element('-DISCOUNT-').update(value="{:.2f}".format(discount_amount))
            window.Element('-INVOICE-AMT-').update(value="{:.2f}".format(invoice_amount))
            window.Element('-PAID-AMT-').update(value="{:.2f}".format(paid_amount))

            db_pos_sql_stmt = (
                "SELECT inv_item.item_code, item_name, barcode, uom, qty,standard_selling_price, applied_selling_price, inv_item.cgst_tax_rate, inv_item.sgst_tax_rate from `tabInvoice Item` inv_item, tabItem item WHERE inv_item.parent = %s and inv_item.item_code = item.item_code")
            db_pos_sql_data = (reference_number,)
            print(db_pos_sql_stmt)
            try:
                db_items = self.db.query(db_pos_sql_stmt, db_pos_sql_data)
            except mariadb.Error as db_err:
                print(f"POS database error - 018: {db_err}")
                #db_pos_conn.close()
                sys.exit(1)

            #db_items = db_pos_cur.fetchall()
            row_item = []
            self.list_items.clear()

            for db_item_row in db_items:
                print('\ndb_item_row:', db_item_row)
                item_code = db_item_row[0]
                item_name = db_item_row[1]
                barcode = db_item_row[2]
                uom = db_item_row[3]
                qty = db_item_row[4]
                selling_price = db_item_row[5]
                cgst_tax_rate = db_item_row[7]
                sgst_tax_rate = db_item_row[8]
                selling_amount = float(qty) * float(selling_price)
                tax_rate = float(cgst_tax_rate) + float(sgst_tax_rate)
                tax_amount = selling_amount * tax_rate / 100
                net_amount = selling_amount + tax_amount
                row_item = []
                row_item.append(item_code)
                row_item.append(barcode)
                row_item.append(item_name)
                row_item.append(uom)
                row_item.append("{:.2f}".format(qty))
                row_item.append("{:.2f}".format(selling_price))
                row_item.append("{:.2f}".format(selling_amount))
                row_item.append("{:.2f}".format(tax_rate))
                row_item.append("{:.2f}".format(tax_amount))
                row_item.append("{:.2f}".format(net_amount))
                row_item.append("{:.2f}".format(cgst_tax_rate))
                row_item.append("{:.2f}".format(sgst_tax_rate))
                print('\nrow_item:', row_item)
                self.list_items.append(row_item)

            window.Element('-TABLE-').update(values=self.list_items)
            print('\nlist_items:', self.list_items)
            self.sum_item_list(window)

    def sortTable(self):
        self.list_items.sort(key=lambda i: i[2])  # sort on third column ascending
        self.list_items.sort(key=lambda i: i[0], reverse=True)  # sort on third column descending


    def initialize_payment_screen(self,popup_payment,window):
        popup_payment['-CUST-NAME-'].Widget.config(takefocus=0)
        popup_payment['-NET-AMT-'].Widget.config(takefocus=0)
        popup_payment['-INVOICE-AMT-'].Widget.config(takefocus=0)
        popup_payment['-TOTAL-PAYMENT-'].Widget.config(takefocus=0)
        popup_payment['-BALANCE-AMT-'].Widget.config(takefocus=0)
        popup_payment['-AVAILABLE-PT-'].Widget.config(takefocus=0)
        popup_payment['-REDEEM-AMT-'].Widget.config(takefocus=0)
        popup_payment['-ROUND-ADJ-'].Widget.config(takefocus=0)
        popup_payment['-ROUNDED-AMT-'].Widget.config(takefocus=0)

        net_amt = float(window.Element('-NET-PRICE-').get())
        rounding_adj = net_amt - round(net_amt, 0)
        rounded_amt = net_amt - rounding_adj
        popup_payment.Element('-NET-AMT-').update(value="{:.2f}".format(net_amt))
        popup_payment.Element('-ROUND-ADJ-').update(value="{:.2f}".format(rounding_adj))
        popup_payment.Element('-ROUNDED-AMT-').update(value="{:.2f}".format(rounded_amt))

        popup_payment.Element('-DISCOUNT-AMT-').update(value="{:.2f}".format(0))
        popup_payment.Element('-INVOICE-AMT-').update(value="{:.2f}".format(rounded_amt))
        popup_payment.Element('-CASH-PAYMENT-').update(value="{:.2f}".format(rounded_amt))
        popup_payment.Element('-CARD-PAYMENT-').update(value="{:.2f}".format(0))
        popup_payment.Element('-TOTAL-PAYMENT-').update(value="{:.2f}".format(rounded_amt))
        popup_payment.Element('-BALANCE-AMT-').update(value="{:.2f}".format(0))
        popup_payment.Element('-MOBILE-NO-').SetFocus()
        popup_payment.Element('-MOBILE-NO-').update(value='0000000000')


    def event_discount_entered(self,popup_payment):
        rounded_amt = popup_payment.Element('-ROUNDED-AMT-').get()
        discount_amt = popup_payment.Element('-DISCOUNT-AMT-').get()
        invoice_amt = float(rounded_amt) - float(discount_amt)
        cash_payment_amt = invoice_amt
        total_payment = invoice_amt
        popup_payment.Element('-INVOICE-AMT-').update(value="{:.2f}".format(invoice_amt))
        popup_payment.Element('-CASH-PAYMENT-').update(value="{:.2f}".format(cash_payment_amt))
        popup_payment.Element('-TOTAL-PAYMENT-').update(value="{:.2f}".format(total_payment))


    def event_cash_card_payment_entered(self,popup_payment):
        retval = 0
        retval = popup_payment.Element('-INVOICE-AMT-').get()
        retval = '0.00' if retval == '' or not retval else retval
        invoice_amt = float(retval)
        retval = popup_payment.Element('-CASH-PAYMENT-').get()
        retval = '0.00' if retval == '' or not retval else retval
        cash_payment_amt = float(retval)
        retval = popup_payment.Element('-CARD-PAYMENT-').get()
        retval = '0.00' if retval == '' or not retval else retval
        card_payment_amt = float(retval)
        total_payment = cash_payment_amt + card_payment_amt
        balance_amt = total_payment - invoice_amt
        popup_payment.Element('-CASH-PAYMENT-').update(value="{:.2f}".format(cash_payment_amt))
        popup_payment.Element('-CARD-PAYMENT-').update(value="{:.2f}".format(card_payment_amt))
        popup_payment.Element('-INVOICE-AMT-').update(value="{:.2f}".format(invoice_amt))
        popup_payment.Element('-TOTAL-PAYMENT-').update(value="{:.2f}".format(total_payment))
        popup_payment.Element('-BALANCE-AMT-').update(value="{:.2f}".format(balance_amt))


    def event_mobile_number_entered(self,popup_payment):
        mobile_number = popup_payment.Element('-MOBILE-NO-').get()
        if mobile_number != '':
            cust_name, loyalty_pts = self.get_cust_details(mobile_number)
            if cust_name != '':
                print('cust:', mobile_number, cust_name, loyalty_pts)
                popup_payment.Element('-CUST-NAME-').update(value=cust_name)
                popup_payment.Element('-AVAILABLE-PT-').update(value=loyalty_pts)
            else:
                sg.popup('Customer not found', keep_on_top=True)
                popup_payment.Element('-MOBILE-NO-').update(value='0000000000')
                popup_payment.Element('-MOBILE-NO-').SetFocus()


    def event_payment_ok_clicked(self,popup_payment,window):
        retval = 0
        mobile_number = popup_payment.Element('-MOBILE-NO-').get()
        net_amt = float(popup_payment.Element('-NET-AMT-').get())
        retval = popup_payment.Element('-DISCOUNT-AMT-').get()
        retval = '0.00' if retval == '' or not retval else retval
        discount_amt = float(retval)
        invoice_amt = net_amt - discount_amt
        retval = popup_payment.Element('-INVOICE-AMT-').get()
        retval = '0.00' if retval == '' or not retval else retval
        invoice_amt = float(retval)
        retval = popup_payment.Element('-CASH-PAYMENT-').get()
        retval = '0.00' if retval == '' or not retval else retval
        cash_payment_amt = float(retval)
        retval = popup_payment.Element('-CARD-PAYMENT-').get()
        retval = '0.00' if retval == '' or not retval else retval
        card_payment_amt = float(retval)

        if mobile_number == '':
            sg.popup('Mobile number is mandatory', keep_on_top=True)
            return
        if cash_payment_amt == 0 and card_payment_amt == 0:
            sg.popup('One of the Payment is mandatory', keep_on_top=True)
            return
        if card_payment_amt > invoice_amt:
            sg.popup('Card amount cannot be more than Invoice amount', keep_on_top=True)
            return

        total_payment = cash_payment_amt + card_payment_amt
        balance_amt = total_payment - invoice_amt
        if balance_amt > 0:
            sg.popup('Invoice amount / Balance unpaid', keep_on_top=True)
            return

        reference_number = window.Element('-REFERENCE_NO-').get()
        retval = popup_payment.Element('-CREDIT-NOTE-').get()
        retval = '0.00' if retval == '' or not retval else retval
        credit_note_amt = float(retval)
        retval = popup_payment.Element('-REDEEM-PT-').get()
        retval = '0' if retval == '' or not retval else retval
        loyalty_points_redeemed = int(retval)
        retval = popup_payment.Element('-REDEEM-AMT-').get()
        retval = '0.00' if retval == '' or not retval else retval
        loyalty_redeemed_amt = float(retval)
        retval = popup_payment.Element('-TOTAL-PAYMENT-').get()
        retval = '0.00' if retval == '' or not retval else retval
        paid_amt = float(retval)

        db_pos_sql_stmt = "SELECT nextval('INVOICE_NUMBER')"
        try:
            db_item_row = self.db.query_one(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error - 002: {db_err}")
            #db_pos_conn.close()
            sys.exit(1)

        if db_item_row is None:
            print('Sequence not found')
        else:
            invoice_number = db_item_row[0]
        print(invoice_number)

        db_pos_sql_stmt = (
            "UPDATE tabInvoice SET invoice_number=%s, posting_date=now(), customer=%s, discount_amount=%s, credit_note_amount=%s, loyalty_points_redeemed=%s, loyalty_redeemed_amount=%s, invoice_amount=%s, paid_amount=%s, modified=now(), modified_by=%s"
            " WHERE name = %s")
        db_pos_sql_data = (
        invoice_number, mobile_number, discount_amt, credit_note_amt, loyalty_points_redeemed, loyalty_redeemed_amt,
        invoice_amt, paid_amt, self.ws_erp_user, reference_number)
        try:
            self.db.query_with_param(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error - 005: {db_err}")
            #db_pos_conn.rollback()
            #db_pos_conn.close()
            sys.exit(1)

        self.db.commit()

        popup_payment.Element('-INVOICE-AMT-').update(value="{:.2f}".format(invoice_amt))
        popup_payment.Element('-TOTAL-PAYMENT-').update(value="{:.2f}".format(total_payment))
        popup_payment.Element('-BALANCE-AMT-').update(value="{:.2f}".format(balance_amt))

        window.Element('-INVOICE_NO-').update(value=invoice_number)
        window.Element('-INVOICE-AMT-').update(value="{:.2f}".format(invoice_amt))
        window.Element('-DISCOUNT-').update(value="{:.2f}".format(discount_amt))
        window.Element('-PAID-AMT-').update(value="{:.2f}".format(total_payment))
        window.Element('-MOBILE_NO-').update(value=mobile_number)
        window.Element('-STATUS-').update(value='PAID', text_color='Green')



    def event_paid_clicked(self,popup_payment):
        net_amt = float(popup_payment.Element('-NET-AMT-').get())
        retval = popup_payment.Element('-DISCOUNT-AMT-').get()
        retval = '0.00' if retval == '' or not retval else retval
        discount_amt = float(retval)
        invoice_amt = net_amt - discount_amt
        retval = popup_payment.Element('-INVOICE-AMT-').get()
        retval = '0.00' if retval == '' or not retval else retval
        invoice_amt = float(retval)
        retval = popup_payment.Element('-CASH-PAYMENT-').get()
        retval = '0.00' if retval == '' or not retval else retval
        cash_payment_amt = float(retval)
        retval = popup_payment.Element('-CARD-PAYMENT-').get()
        retval = '0.00' if retval == '' or not retval else retval
        card_payment_amt = float(retval)
        total_payment = cash_payment_amt + card_payment_amt
        balance_amt = total_payment - invoice_amt
        if balance_amt:
            cash_payment_amt = cash_payment_amt - balance_amt
            balance_amt = 0
        total_payment = cash_payment_amt + card_payment_amt

        popup_payment.Element('-CASH-PAYMENT-').update(value="{:.2f}".format(cash_payment_amt))
        popup_payment.Element('-INVOICE-AMT-').update(value="{:.2f}".format(invoice_amt))
        popup_payment.Element('-TOTAL-PAYMENT-').update(value="{:.2f}".format(total_payment))
        popup_payment.Element('-BALANCE-AMT-').update(value="{:.2f}".format(balance_amt))

    def get_cust_details(self,mobile_number):
        customer_name = ''
        loyalty_points = 0
        db_pos_sql_stmt = "SELECT customer_name, loyalty_points from tabCustomer where mobile_number = %s"
        db_pos_sql_data = (mobile_number,)
        try:
            db_cust_row = self.db.query_with_param(db_pos_sql_stmt, db_pos_sql_data)
        except mariadb.Error as db_err:
            print(f"POS database error - 001: {db_err}")
            #db_pos_conn.close()
            #sys.exit(1)

        #db_cust_row = db_pos_cur.fetchone()
        if db_cust_row is None:
            return '', 0

        customer_name = db_cust_row[0]
        loyalty_points = db_cust_row[1]
        return customer_name, loyalty_points