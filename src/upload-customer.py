##################################################
# Application: alignPOS
# Installation: AFSM
# CLI Program: upload-customer
# Description: Send the list of all Customers along with details
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
print_log('alignPOS - Upload Customer - Version 1.1')
print_log('----------------------------------------')

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
# Delete old Customer records
db_pos_sql_stmt = (
    "DELETE FROM tabCustomer"
)

try:
    db_pos_cur.execute(db_pos_sql_stmt)
    db_pos_conn.commit()
    print_log("Old Customer records Deleted")
except mariadb.Error as db_err:
    print_log(f"POS database error: {db_err}")
    db_pos_conn.rollback()
    sys.exit(1)


######
# Fetch List of Customers from ERP
ws_erp_method = '/api/resource/Customer?limit_page_length=None'
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
# Fetch each Customer from Customer List from ERP   
cust_count = 0
for ws_erp_row_cust in ws_erp_resp_json["data"]:
    cust_count+=1
    ws_erp_method = '/api/resource/Customer/' + ws_erp_row_cust["name"] + '?fields=["*"]'
    try:
        ws_erp_resp = ws_erp_sess.get(ws_erp_host + ws_erp_method)
        ws_erp_resp.raise_for_status()   
        ws_erp_resp_text = ws_erp_resp.text
        ws_erp_resp_json = json.loads(ws_erp_resp_text)
        #print_log(ws_erp_resp_json["data"]["name"])
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

    cust_name = ws_erp_resp_json["data"]["name"]
    cust_cust_name = ws_erp_resp_json["data"]["customer_name"]
    cust_type = ws_erp_resp_json["data"]["customer_type"]
    cust_address = ws_erp_resp_json["data"]["address"]
    cust_mobile_number = ws_erp_resp_json["data"]["mobile_number"]
    cust_loyalty_points = ws_erp_resp_json["data"]["loyalty_points"]
    
    db_pos_sql_stmt = (
       "INSERT INTO tabCustomer (name, customer_name, customer_type, address, mobile_number, loyalty_points, creation, owner)"
       "VALUES (%s, %s, %s, %s, %s, %s, now(), %s)"
    )
    db_pos_sql_data = (cust_name, cust_cust_name, cust_type, cust_address, cust_mobile_number, cust_loyalty_points, ws_erp_user)

    try:
        db_pos_cur.execute(db_pos_sql_stmt, db_pos_sql_data)
        db_pos_conn.commit()
        print_log(f"Inserted Customer: {cust_name}")
    except mariadb.Error as db_err:
        print_log(f"POS database error: {db_err}")
        db_pos_conn.rollback()
        sys.exit(1)


print_log(f"Total Customers Inserted: {cust_count}")

######    
# Closing DB connection
db_pos_conn.close()
 
print_log("Customer Upload process completed")
file_log.close()
