import pymysql

class Database:
    def __init__(self, db_name, db_password, db_user, db_port, db_host):
        self.db_name = db_name
        self.db_password = db_password
        self.db_user = db_user
        self.db_port = db_port
        self.db_host = db_host
        self.connection = self.connect

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

    def user_registration(self, username, telegram_id, phone, coordinates):
        sql = """
        INSERT INTO users (username, telegram_id, phone_number, coordinates) 
        VALUES (%s, %s, %s, %s) 
        """
        params = (username, telegram_id, phone, coordinates)
        return self.execute(sql, params, commit=True)

    def detect_user(self, telegram_id):
        sql = """SELECT * FROM users WHERE telegram_id = %s"""
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
        
    def detect_admin(self, telegram_id):
        sql = """SELECT * FROM admin WHERE telegram_id = %s"""
        params = (telegram_id,)
        return self.execute(sql,params,fetchone=True)
    
    def category_creation(self,name,image_id,description):
        sql = """Insert into categories (name,image_id,description) values(%s,%s,%s)"""
        params = (name,image_id,description)

        try: 
            return self.execute(sql,params,commit = True)
        except Exception as e:
            print(f"Bazada xatolik(category_add:{e}")
            return False
        
    def update_category_all_fields(self, cat_id, name, image_id, description):
        sql = "UPDATE categories SET name=%s, image_id=%s, description=%s WHERE id=%s"
        params = (name, image_id, description, cat_id)

        return self.execute(sql, params, commit=True)

    def get_all_categories(self):
        sql = "SELECT id, name FROM categories"
        return self.execute(sql, fetchall=True)
    
    def delete_category(self,cat_id):
        sql = "delete from categories where id = %s"
        params = (cat_id,)
        return self.execute(sql,params,commit = True)
    
    def delete_admin(self,admin_id):
        sql = "delete from admin where id = %s"
        params = (admin_id,)
        return self.execute(sql,params,commit = True)

    def get_all_admins(self):
        sql = "SELECT id, username FROM admin"
        return self.execute(sql, fetchall=True)
        
    def add_new_product(self,category_id,name,description,price,image_id):
        sql = "Insert into products (category_id,name,description,price,image_id) values (%s,%s,%s,%s,%s)"
        params = (category_id,name,description,price,image_id)

        try:
            self.execute(sql,params,commit=True)
            return True
        except Exception as e:
            print(f"Bazada xatolik(category_add:{e}")
            return False

    def get_products_by_category(self, cat_id):
        sql = "SELECT * FROM products WHERE category_id = %s"
        return self.execute(sql, (cat_id,), fetchall=True)
    
    def delete_product(self,product_id):
        sql = "DELETE * FROM products WHERE id = %s"
        return self.execute(sql, (product_id,),commit = True)
    