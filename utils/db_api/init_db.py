import asyncio
import logging
from loader import db  # db obyekti Database klassidan olingan deb hisoblaymiz

async def create_tables():
    # 1. Foydalanuvchilar
    sql_users = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        telegram_id VARCHAR(50) UNIQUE NOT NULL,
        phone_number VARCHAR(20),
        coordinates TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # 2. Adminlar
    sql_admins = """
    CREATE TABLE IF NOT EXISTS admin (
        id INT AUTO_INCREMENT PRIMARY KEY,
        telegram_id VARCHAR(50) UNIQUE NOT NULL,
        username VARCHAR(255),
        phone VARCHAR(20)
    );
    """

    # 3. Kategoriyalar
    sql_categories = """
    CREATE TABLE IF NOT EXISTS categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        image_id VARCHAR(255),
        description TEXT
    );
    """

    # 4. Mahsulotlar
    sql_products = """
    CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category_id INT,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        price DECIMAL(15, 2) NOT NULL,
        image_id VARCHAR(255),
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
    );
    """

    # 5. Kuryerlar
    sql_couriers = """
    CREATE TABLE IF NOT EXISTS couriers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        telegram_id VARCHAR(50) UNIQUE NOT NULL,
        username VARCHAR(100),
        phone VARCHAR(20)
    );
    """

    # 6. Savatcha
    sql_cart = """
    CREATE TABLE IF NOT EXISTS cart (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(50),
        product_id INT,
        quantity INT DEFAULT 1,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    );
    """

    # 7. Buyurtmalar
    sql_orders = """
    CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(50),
        courier_id VARCHAR(50),
        total_price DECIMAL(15, 2),
        delivery_price DECIMAL(10, 2) DEFAULT 0,
        distance_km DECIMAL(10, 2) DEFAULT 0,
        status VARCHAR(50) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    # 8. Buyurtma mahsulotlari
    sql_order_items = """
    CREATE TABLE IF NOT EXISTS order_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        product_id INT,
        quantity INT,
        price DECIMAL(15, 2),
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    );
    """

    # 9. Kuryer takliflari (Bids)
    sql_order_bids = """
    CREATE TABLE IF NOT EXISTS order_bids (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        courier_id VARCHAR(50),
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    );
    """

    # 10. Restoranlar
    sql_restaurants = """
    CREATE TABLE IF NOT EXISTS restaurants (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        address VARCHAR(255),
        latitude DECIMAL(10, 8),
        longitude DECIMAL(11, 8),
        description TEXT
    );
    """

    tables = [
        sql_users, sql_admins, sql_categories, sql_products, 
        sql_couriers, sql_cart, sql_orders, sql_order_items, 
        sql_order_bids, sql_restaurants
    ]

    for table_sql in tables:
        try:
            db.execute(table_sql, commit=True)
        except Exception as e:
            logging.error(f"Xatolik jadval yaratishda: {e}")

    # Mavjud orders jadvaliga ustunlar qo'shish (agar jadval oldin bor bo'lsa)
    alter_queries = [
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS courier_id VARCHAR(50)",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS delivery_price DECIMAL(10,2) DEFAULT 0",
        "ALTER TABLE orders ADD COLUMN IF NOT EXISTS distance_km DECIMAL(10,2) DEFAULT 0"
    ]
    
    for query in alter_queries:
        try:
            db.execute(query, commit=True)
        except:
            pass

    print("Barcha jadvallar muvaffaqiyatli yaratildi!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(create_tables())