import mariadb
import datetime
import json
import sys
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


    def proc_barcode(self,barcode, winObj):
        if len(barcode) > 12:
            print('barcode=', barcode)
            # db_pos_cur.execute("SELECT item_code, item_name, uom, selling_price, cgst_tax_rate, sgst_tax_rate from tabItem where barcode = '" + barcode + "'")
            # db_item_row = db_pos_cur.fetchone()
            db_item_row = self.dbOperation.getItemDetails(barcode)
            if db_item_row is None:
                print('Item not found')
            else:
                item_code = db_item_row[0]
                item_name = db_item_row[1]
                uom = db_item_row[2]
                qty = 1
                selling_price = db_item_row[3]
                cgst_tax_rate = db_item_row[4]
                sgst_tax_rate = db_item_row[5]
                print(item_name)
                row_item = []
                row_item.append(item_code)
                row_item.append(barcode)
                row_item.append(item_name)
                row_item.append(uom)
                row_item.append(qty)
                row_item.append("{:.2f}".format(selling_price))
                selling_amount = float(qty) * float(selling_price)
                row_item.append("{:.2f}".format(selling_amount))
                tax_rate = float(cgst_tax_rate) + float(sgst_tax_rate)
                row_item.append(tax_rate)
                tax_amount = selling_amount * tax_rate / 100
                row_item.append("{:.2f}".format(tax_amount))
                net_price = selling_amount + tax_amount
                row_item.append("{:.2f}".format(net_price))
                self.list_items.append(row_item)
                print(self.list_items)
                winObj.Element('-TABLE-').update(values=self.list_items)
                winObj.Element('-BARCODE-NB-').update(value='')
                winObj.Element('-ITEMNAME-').update(value='')
                winObj.Element('-BARCODE-NB-').set_focus()
                self.sum_item_list(winObj)

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

        reference_number = winObj.Element('-REFERENCE_NO-').get()
        if reference_number == '' and len(self.list_items) > 0:
            self.insert_invoice(winObj)
        else:
            self.update_invoice(winObj)


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
            print(f"POS database error: {db_err}")
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
            print(f"POS database error: {db_err}")
            #self.db.rollback()
            #self.db.close()
            sys.exit(1)

        item_count = 0
        for row_item in self.list_items:
            item_count += 1
            item_code = row_item[0]
            qty = row_item[4]
            selling_price = row_item[6]
            cgst_tax_rate = 0.0 #row_item[10]
            sgst_tax_rate = 0.0 #row_item[11]
            name = reference_number + f"{item_count:04d}"
            print(name)

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
                print(f"POS database error1: {db_err}")
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
        total_cgst = 0
        total_sgst = 0
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
        window.Element('-TABLE-').update(values=self.list_items)
        window.Element('-INVOICE_NO-').update(value='')
        window.Element('-REFERENCE_NO-').update(value='')
        window.Element('-MOBILE_NO-').update(value='')


    def update_invoice(self,window):
        print('update')
        reference_number = window.Element('-REFERENCE_NO-').get()
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
            print(f"POS database error: {db_err}")
            #db_pos_conn.rollback()
            #db_pos_conn.close()
            sys.exit(1)
        print('here1', reference_number)
        db_pos_sql_stmt = ("DELETE FROM `tabInvoice Item` WHERE parent = '" + reference_number + "'")

        try:
            self.db.execute(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")
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
                print(f"POS database error: {db_err}")
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
            print(f"POS database error: {db_err}")
            #db_pos_conn.rollback()
            #db_pos_conn.close()
            sys.exit(1)

        db_pos_sql_stmt = ("DELETE FROM `tabInvoice` WHERE name = '" + reference_number + "'")
        try:
            self.db.execute(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")
            #db_pos_conn.rollback()
            #db_pos_conn.close()
            sys.exit(1)
        self.db.commit()


    def goto_previous_invoice(self,window):
        print('prev')
        reference_number = window.Element('-REFERENCE_NO-').get()
        if (reference_number == ''):
            db_pos_sql_stmt = (
                "SELECT name, posting_date, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount from tabInvoice WHERE name = (select max(name) from tabInvoice)")
            try:
                self.db.execute(db_pos_sql_stmt)
            except mariadb.Error as db_err:
                print(f"POS database error: {db_err}")
                #db_pos_conn.close()
                sys.exit(1)
        else:
            db_pos_sql_stmt = (
                "SELECT name, posting_date, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount from tabInvoice WHERE name = (select max(name) from tabInvoice where name < %s)")
            db_pos_sql_data = (reference_number,)

            try:
                self.db.execute(db_pos_sql_stmt, db_pos_sql_data)
            except mariadb.Error as db_err:
                print(f"POS database error: {db_err}")
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
                print(f"POS database error: {db_err}")
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

    def goto_next_invoice(self,window):
        print('next')
        reference_number = window.Element('-REFERENCE_NO-').get()
        if (reference_number == ''):
            return
        else:
            db_pos_sql_stmt = (
                "SELECT name, posting_date, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount from tabInvoice WHERE name = (select min(name) from tabInvoice where name > %s)")
            db_pos_sql_data = (reference_number,)

            try:
                self.db.execute(db_pos_sql_stmt, db_pos_sql_data)
            except mariadb.Error as db_err:
                print(f"POS database error: {db_err}")
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
                print(f"POS database error: {db_err}")
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

    def goto_last_invoice(self,window):
        print('last')
        db_pos_sql_stmt = (
            "SELECT name, posting_date, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount from tabInvoice WHERE name = (select max(name) from tabInvoice)")

        try:
            self.db.execute(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")
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
                print(f"POS database error: {db_err}")
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
                self.db.list_items.append(row_item)
                window.Element('-TABLE-').update(values=self.list_items)
            self.sum_item_list(window)

    def goto_first_invoice(self,window):
        print('first')
        db_pos_sql_stmt = (
            "SELECT name, posting_date, customer, total_amount, cgst_tax_amount, sgst_tax_amount, invoice_amount from tabInvoice WHERE name = (select min(name) from tabInvoice)")

        try:
            self.db.execute(db_pos_sql_stmt)
        except mariadb.Error as db_err:
            print(f"POS database error1: {db_err}")
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
                print(f"POS database error2: {db_err}")
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
