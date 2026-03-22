import pymysql


class Database:
    def __init__(self, db_name, db_password, db_user, db_port, db_host):
        self.db_name = db_name
        self.db_password = db_password
        self.db_user = db_user
        self.db_port = db_port
        self.db_host = db_host

    def connect(self):
        return pymysql.Connection(
            database=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            cursorclass=pymysql.cursors.DictCursor
        )

    def execute(self, sql: str, params: tuple = (), commit=False, fetchone=False, fetchall=False) -> dict | list:
        database = self.connect()
        cursor = database.cursor()

        cursor.execute(sql, params)
        data = None

        if fetchone:
            data = cursor.fetchone()

        elif fetchall:
            data = cursor.fetchall()

        if commit:
            database.commit()

        return data

    def user_registration(self, username, telegram_id, phone, lng, lat):
        sql = """
        INSERT INTO user (username, telegram_id, phone_number, logitude, latitude) 
        VALUES (%s, %s, %s, %s, %s) 
        """
        params = (username, telegram_id, phone, lng, lat)
        return self.execute(sql, params, commit=True)

    def detect_user(self, telegram_id):
        sql = """SELECT * FROM user WHERE telegram_id = %s"""
        params = (telegram_id,)
        return self.execute(sql, params, fetchone=True)

    def add_admin(self, telegram_id, username, phone):
        sql = "INSERT INTO admin (telegram_id, username, phone) VALUES (%s, %s, %s)"
        params = (telegram_id, username, phone)

        try:
            return self.execute(sql, params, commit=True)
        except Exception as e:
            print(f"Bazada xatolik (add_admin): {e}")
            return False



