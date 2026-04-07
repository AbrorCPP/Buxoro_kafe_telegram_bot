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

    def get_all_admin_ids(self):
        sql = "SELECT telegram_id FROM admin"
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
        sql = "DELETE FROM products WHERE id = %s"
        return self.execute(sql, (product_id,),commit = True)

    def get_product(self, product_id):
        sql = "SELECT id, category_id, name, description, price, image_id FROM products WHERE id = %s"
        return self.execute(sql, (product_id,), fetchone=True)

    def add_to_cart(self, telegram_id, product_id, quantity=1):
        sql_check = "SELECT id, quantity FROM cart WHERE user_id = %s AND product_id = %s"
        res = self.execute(sql_check, (telegram_id, product_id), fetchone=True)
        if res:
            sql = "UPDATE cart SET quantity = quantity + %s WHERE id = %s"
            return self.execute(sql, (quantity, res['id']), commit=True)
        else:
            sql = "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)"
            return self.execute(sql, (telegram_id, product_id, quantity), commit=True)

    def get_cart(self, telegram_id):
        sql = """
        SELECT c.id as cart_id, c.product_id, c.quantity, p.name, p.price 
        FROM cart c 
        JOIN products p ON c.product_id = p.id 
        WHERE c.user_id = %s
        """
        return self.execute(sql, (telegram_id,), fetchall=True)

    def clear_cart(self, telegram_id):
        sql = "DELETE FROM cart WHERE user_id = %s"
        return self.execute(sql, (telegram_id,), commit=True)

    def delete_cart_item(self, cart_id):
        sql = "DELETE FROM cart WHERE id = %s"
        return self.execute(sql, (cart_id,), commit=True)

    def create_order(self, telegram_id, items, total_price, delivery_price=0, distance=0):
        sql_order = "INSERT INTO orders (user_id, total_price, delivery_price, distance_km) VALUES (%s, %s, %s, %s)"
        self.execute(sql_order, (telegram_id, total_price, delivery_price, distance), commit=True)
        
        sql_last = "SELECT id FROM orders WHERE user_id = %s ORDER BY id DESC LIMIT 1"
        order_res = self.execute(sql_last, (telegram_id,), fetchone=True)
        if not order_res:
            return False
        order_id = order_res['id']
        
        for item in items:
            sql_item = "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)"
            self.execute(sql_item, (order_id, item['product_id'], item['quantity'], item['price']), commit=True)
        return order_id

    def add_courier(self, telegram_id, username, phone):
        sql = "INSERT INTO couriers (telegram_id, username, phone) VALUES (%s, %s, %s)"
        return self.execute(sql, (telegram_id, username, phone), commit=True)

    def get_all_couriers(self):
        sql = "SELECT * FROM couriers"
        return self.execute(sql, fetchall=True)

    def detect_courier(self, telegram_id):
        sql = "SELECT * FROM couriers WHERE telegram_id = %s"
        return self.execute(sql, (telegram_id,), fetchone=True)

    def delete_courier(self, telegram_id):
        sql = "DELETE FROM couriers WHERE telegram_id = %s"
        return self.execute(sql, (telegram_id,), commit=True)

    def assign_courier(self, order_id, courier_id):
        # check if already assigned
        sql_chk = "SELECT courier_id FROM orders WHERE id = %s"
        order = self.execute(sql_chk, (order_id,), fetchone=True)
        if order and order['courier_id']:
            return False # Already assigned
        sql = "UPDATE orders SET courier_id = %s, status = 'accepted_by_courier' WHERE id = %s"
        self.execute(sql, (courier_id, order_id), commit=True)
        return True

    def update_order_status(self, order_id, status):
        sql = "UPDATE orders SET status = %s WHERE id = %s"
        return self.execute(sql, (status, order_id), commit=True)

    def get_order(self, order_id):
        sql = "SELECT * FROM orders WHERE id = %s"
        return self.execute(sql, (order_id,), fetchone=True)

    def get_order_items_text(self, order_id):
        sql = """
        SELECT p.name, oi.quantity, oi.price 
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = %s
        """
        items = self.execute(sql, (order_id,), fetchall=True)
        text = ""
        for i in items:
            text += f"▫️ {i['name']} x {i['quantity']} = {i['price'] * i['quantity']} so'm\n"
        return text

    def add_order_bid(self, order_id, courier_id):
        sql_check = "SELECT id FROM order_bids WHERE order_id=%s AND courier_id=%s"
        if self.execute(sql_check, (order_id, courier_id), fetchone=True):
            return False
        sql = "INSERT INTO order_bids (order_id, courier_id) VALUES (%s, %s)"
        return self.execute(sql, (order_id, courier_id), commit=True)

    def get_order_bids(self, order_id):
        sql = "SELECT b.courier_id, c.username, c.phone FROM order_bids b JOIN couriers c ON b.courier_id = c.telegram_id WHERE b.order_id = %s"
        return self.execute(sql, (order_id,), fetchall=True)