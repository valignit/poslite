##################################################
# alignPOS - Upload Item
# Version: 1.0
# 1.0.0 - 25-04-2021: New program
##################################################

import json
import requests
import mariadb
import sys
import datetime


##############################
# Main
##############################
print('\nalignPOS - Upload Item - Version 1.0')
print('------------------------------------')

######
# Connect to ERPNext web service
ws_erp_host = "http://104.236.110.12/"
ws_erp_sess = requests.Session()
ws_erp_user = "administrator"
ws_erp_passwd = "VAlignIt@2021ad"
ws_erp_cred = {"usr": ws_erp_user, "pwd": ws_erp_passwd }

ws_erp_method = '/api/method/login'

try:
    ws_erp_resp = ws_erp_sess.post(ws_erp_host + ws_erp_method, json=ws_erp_cred)
    ws_erp_resp.raise_for_status()   
    ws_erp_resp_text = ws_erp_resp.text
    ws_erp_resp_json = json.loads(ws_erp_resp_text)
    print(f"ERP web service logged in by {ws_erp_resp_json['full_name']}")
except requests.exceptions.HTTPError as ws_err:
    print(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.ConnectionError as ws_err:
    print(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.Timeout as ws_err:
    print(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.RequestException as ws_err:
    print(f"ERP web service error: {ws_err}")
    sys.exit(1)

######
# Connect to POS database
db_pos_host = "localhost"
db_pos_port = 3306
db_pos_name = "alignpos"
db_pos_user = "alignpos"
db_pos_passwd = "valignit@2021"

try:
    db_pos_conn = mariadb.connect(
        user = db_pos_user,
        password = db_pos_passwd,
        host = db_pos_host,
        port = db_pos_port,
        database = db_pos_name
    )
    print("POS database connected")

except mariadb.Error as db_err:
    print(f"POS database error: {db_err}")
    sys.exit(1)
    
db_pos_cur = db_pos_conn.cursor()


######
# Delete old Item records
db_pos_sql_stmt = (
    "DELETE FROM tabItem"
)

try:
    db_pos_cur.execute(db_pos_sql_stmt)
    db_pos_conn.commit()
    print("Old Item records Deleted")
except mariadb.Error as db_err:
    print(f"POS database error: {db_err}")
    db_pos_conn.rollback()
    sys.exit(1)


######
# Fetch List of Items from ERP
ws_erp_method = '/api/resource/Item?limit_page_length=None'
try:
    ws_erp_resp = ws_erp_sess.get(ws_erp_host + ws_erp_method)
    ws_erp_resp.raise_for_status()   
    ws_erp_resp_text = ws_erp_resp.text
    ws_erp_resp_json = json.loads(ws_erp_resp_text)
    #print(ws_erp_resp_json["data"])
except requests.exceptions.HTTPError as ws_err:
    print(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.ConnectionError as ws_err:
    print(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.Timeout as ws_err:
    print(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.RequestException as ws_err:
    print(f"ERP web service error: {ws_err}")
    sys.exit(1)


######
# Fetch each Item from Item List from ERP   
item_count = 0
for ws_erp_row_item in ws_erp_resp_json["data"]:
    item_count+=1
    ws_erp_method = '/api/resource/Item/' + ws_erp_row_item["name"]
    try:
        ws_erp_resp = ws_erp_sess.get(ws_erp_host + ws_erp_method)
        ws_erp_resp.raise_for_status()   
        ws_erp_resp_text = ws_erp_resp.text
        ws_erp_resp_json = json.loads(ws_erp_resp_text)
        #print(ws_erp_resp_json["data"]["name"])
    except requests.exceptions.HTTPError as ws_err:
        print(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.ConnectionError as ws_err:
        print(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.Timeout as ws_err:
        print(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.RequestException as ws_err:
        print(f"ERP web service error: {ws_err}")
        sys.exit(1)

    item_name = ws_erp_resp_json["data"]["name"]
    item_code = ws_erp_resp_json["data"]["item_code"]
    item_item_name = ws_erp_resp_json["data"]["item_name"]
    item_group = ws_erp_resp_json["data"]["item_group"]
    item_stock = ws_erp_resp_json["data"]["shop_stock"]
    item_selling_price = ws_erp_resp_json["data"]["standard_rate"]
    
    # Pick first uom of the Item 
    for uom in ws_erp_resp_json["data"]["uoms"]:
        item_uom = uom["uom"]
        #print(item_uom)
        break

    # Pick first barcode of the Item 
    for barcode in ws_erp_resp_json["data"]["barcodes"]:
        item_barcode = barcode["name"]
        #print(item_barcode)
        break

    # Pick first Tax template of the Item     
    for tax in ws_erp_resp_json["data"]["taxes"]:
        item_tax_template = tax["item_tax_template"]
        #print(item_tax_template)        
        break

    # Fetch Item Tax Template details 
    ws_erp_method = '/api/resource/Item Tax Template/' 
    try:
        ws_erp_resp = ws_erp_sess.get(ws_erp_host + ws_erp_method + item_tax_template)
        ws_erp_resp.raise_for_status()   
        ws_erp_resp_text = ws_erp_resp.text
        ws_erp_resp_json = json.loads(ws_erp_resp_text)
        #print(ws_erp_resp_json["data"])
    except requests.exceptions.HTTPError as ws_err:
        print(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.ConnectionError as ws_err:
        print(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.Timeout as ws_err:
        print(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.RequestException as ws_err:
        print(f"ERP web service error: {ws_err}")
        sys.exit(1)

    # Pick first Tax rate from Tax Template
    for tax in ws_erp_resp_json["data"]["taxes"]:
        item_tax_rate = tax["tax_rate"]
        #print(item_tax_rate)        
        break

    db_pos_sql_stmt = (
       "INSERT INTO tabItem (name, item_code, item_name, item_group, barcode, uom, stock, selling_price, item_tax_rate, creation, owner)"
       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s)"
    )
    db_pos_sql_data = (item_name, item_code, item_item_name, item_group, item_barcode, item_uom, item_stock, item_selling_price, item_tax_rate, ws_erp_user)

    try:
        db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        db_pos_conn.commit()
        print("Inserted Item: ", item_name, end = "\r")
    except mariadb.Error as db_err:
        print(f"POS database error: {db_err}")
        db_pos_conn.rollback()
        sys.exit(1)

print("Total Items Inserted: ", item_count)

######    
# Closing DB connection
db_pos_conn.close()
 
print ("Item Upload process completed")

