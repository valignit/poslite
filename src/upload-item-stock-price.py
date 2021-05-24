##################################################
# Application: alignPOS
# Installation: AFSM
# CLI Program: upload-item-stock-price
# Description: Send the latest Item Stock and Price which got updated after the last API call
# Version: 1.0
# 1.0.0 - 25-04-2021: New program
##################################################

import json
import requests
import mariadb
import sys
import datetime


now = datetime.datetime.now()

with open('./alignpos.json') as file_config:
  config = json.load(file_config)
  
file_name = str(__file__)[:-3] + "-" + now.strftime("%Y%m%d%H%M") + ".log"
file_log = open(file_name, "w")

##############################
# Print and Log
##############################
def print_log(msg):
    print(msg)
    msg = str(now) + ': ' + msg + '\n'
    file_log.write(msg)


##############################
# Main
##############################
print_log('alignPOS - Upload Item Stock Price - Version 1.0')
print_log('------------------------------------------------')

######
# Connect to ERPNext web service
ws_erp_host = config["ws_erp_host"]
ws_erp_sess = requests.Session()
ws_erp_user = config["ws_erp_user"]
ws_erp_passwd = config["ws_erp_passwd"]
ws_erp_payload = {"usr": ws_erp_user, "pwd": ws_erp_passwd }

ws_erp_method = '/api/method/login'

try:
    ws_erp_resp = ws_erp_sess.post(ws_erp_host + ws_erp_method, data=ws_erp_payload)
    ws_erp_resp.raise_for_status()   
    ws_erp_resp_text = ws_erp_resp.text
    ws_erp_resp_json = json.loads(ws_erp_resp_text)
    print_log(f"ERP web service logged in by {ws_erp_resp_json['full_name']}")
except requests.exceptions.HTTPError as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.ConnectionError as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.Timeout as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.RequestException as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)

######
# Connect to POS database
db_pos_host = config["db_pos_host"]
db_pos_port = config["db_pos_port"]
db_pos_name = config["db_pos_name"]
db_pos_user = config["db_pos_user"]
db_pos_passwd = config["db_pos_passwd"]

try:
    db_pos_conn = mariadb.connect(
        user = db_pos_user,
        password = db_pos_passwd,
        host = db_pos_host,
        port = db_pos_port,
        database = db_pos_name
    )
    print_log("POS database connected")

except mariadb.Error as db_err:
    print_log(f"POS database error: {db_err}")
    sys.exit(1)
    
db_pos_cur = db_pos_conn.cursor()


######
# Fetch List of Items from ERP
ws_erp_method = '/api/method/get_item_stock_price?limit_page_length=None'
try:
    ws_erp_resp = ws_erp_sess.get(ws_erp_host + ws_erp_method)
    ws_erp_resp.raise_for_status()   
    ws_erp_resp_text = ws_erp_resp.text
    ws_erp_resp_json = json.loads(ws_erp_resp_text)
    #print_log(ws_erp_resp_json["data"])
except requests.exceptions.HTTPError as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.ConnectionError as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.Timeout as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)
except requests.exceptions.RequestException as ws_err:
    print_log(f"ERP web service error: {ws_err}")
    sys.exit(1)


######
# Fetch each Item from Item List from ERP   
item_count = 0
for ws_erp_row_item in ws_erp_resp_json["items"]:
    item_count+=1
    item_name = ws_erp_row_item["item_name"]
    item_code = ws_erp_row_item["item_code"]
    item_stock = ws_erp_row_item["shop_stock"]
    item_selling_price = ws_erp_row_item["standard_rate"]
    item_maximum_retail_price = ws_erp_row_item["maximum_retail_price"]

    db_pos_sql_stmt = (
        "UPDATE tabItem SET stock = %s, selling_price = %s, maximum_retail_price = %s, modified = now(), modified_by = %s WHERE item_code = %s"
    )
    db_pos_sql_data = (item_stock, item_selling_price, item_maximum_retail_price, ws_erp_user, item_code)

    try:
        db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        db_pos_conn.commit()
        print_log(f"Updated Item: {item_code}")
    except mariadb.Error as db_err:
        print_log(f"POS database error: {db_err}")
        db_pos_conn.rollback()
        sys.exit(1)

last_update_date_time = ws_erp_resp_json["date"]

if (item_count > 0):
    ######
    # Update Last update date time
    ws_erp_payload = {"date": last_update_date_time }

    ws_erp_method = '/api/method/put_item_sync_date_time'
    try:
        ws_erp_resp = ws_erp_sess.put(ws_erp_host + ws_erp_method, json=ws_erp_payload)
        ws_erp_resp.raise_for_status()   
        ws_erp_resp_text = ws_erp_resp.text
        ws_erp_resp_json = json.loads(ws_erp_resp_text)
        #print_log(ws_erp_resp_json["data"])
    except requests.exceptions.HTTPError as ws_err:
        print_log(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.ConnectionError as ws_err:
        print_log(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.Timeout as ws_err:
        print_log(f"ERP web service error: {ws_err}")
        sys.exit(1)
    except requests.exceptions.RequestException as ws_err:
        print_log(f"ERP web service error: {ws_err}")
        sys.exit(1)

print_log(f"Total Items Updated: {item_count}")

######    
# Closing DB connection
db_pos_conn.close()

######    
# Closing Log file 
print_log("Item Stock Price Upload process completed")
file_log.close()
