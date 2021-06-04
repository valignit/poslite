import mariadb
import sys
import json

class DBManager:


    with open('./alignpos.json') as file_config:
        data = json.load(file_config)

    db_pos_host = data['db_pos_host']
    db_pos_port = data['db_pos_port']
    db_pos_name = data['db_pos_name']
    db_pos_user = data['db_pos_user']
    db_pos_passwd = data['db_pos_passwd']
    ws_erp_user = data["ws_erp_user"]


    def __init__(self):

        try:
            self._db_pos_conn = mariadb.connect(
                user=self.db_pos_user,
                password=self.db_pos_passwd,
                host=self.db_pos_host,
                port=self.db_pos_port,
                database=self.db_pos_name
            )
            print("POS database connected")
        except mariadb.Error as db_err:
            print(f"POS database error: {db_err}")
            sys.exit(1)

        self._cursor = self._db_pos_conn.cursor()


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._db_pos_conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def execute1(self, sql):
        self.cursor.execute(sql)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def query(self, sql):
        self.cursor.execute(sql)
        return self.fetchall()