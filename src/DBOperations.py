import mariadb

class DBOperations:

    db_pos_host = "localhost"
    db_pos_port = 3306
    db_pos_name = "alignpos"
    db_pos_user = "alignpos"
    db_pos_passwd = "valignit@2021"
    db_pos_conn = None
    db_pos_cur = None

    def __init__(self,server,port,dbname,user,pwd):
        db_pos_host = server
        db_pos_port = port
        db_pos_name = dbname
        db_pos_user = user
        db_pos_passwd = pwd


    try:
        db_pos_conn = mariadb.connect(
            user=db_pos_user,
            password=db_pos_passwd,
            host=db_pos_host,
            port=db_pos_port,
            database=db_pos_name
        )
        print("POS database connected")
    except mariadb.Error as db_err:
        print(f"POS database error: {db_err}")
        sys.exit(1)
    db_pos_cur = db_pos_conn.cursor()


    def fetchItemData(self,barcode):
        query = "SELECT barcode,item_name, uom, FORMAT(selling_price,2),FORMAT(item_tax_rate,2),FORMAT(item_tax_rate,2),FORMAT(item_tax_rate,2),FORMAT(item_tax_rate,2) FROM tabItem where barCode='" + barcode + "';"
        try:
            #self.getDBConnection
            db_pos_cur = self.db_pos_conn.cursor()
            db_pos_cur.execute(query)
            # print('fetchdata=', db_pos_cur.fetchall())
            # for row in db_pos_cur.fetchall():
            #    print(row)
            # Returns a list of lists
            from_db = []
            for result in db_pos_cur.fetchall():
                result = list(result)
                print('result=', result)
                from_db.append(result)
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")
            self.db_pos_conn.rollback()
            sys.exit(1)

        return list(from_db)

    def closeDBCon(self):
        db_pos_conn.close()
