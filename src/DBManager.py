import mariadb
import sys

class DBManager:

    def __init__(self):
        print('db initialized')

    #db_pos_cur = db_pos_conn.cursor()

    @staticmethod
    def getDBConnection(dbhost, dbport, dbname, dbuser, dbpwd):
        try:
                db_pos_conn = mariadb.connect(
                    user=dbuser,
                    password=dbpwd,
                    host=dbhost,
                    port=dbport,
                    database=dbname
                )
                print("POS database connected")
                return db_pos_conn
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")
            sys.exit(1)


"""
    def verifyUser(user,pwd):
        db_pos_cur.execute('select * from tabUser where user_id='+user + ' and password='+pwd)
        userDetail = db_pos_cur.fetchall()
        print(userDetail)
"""