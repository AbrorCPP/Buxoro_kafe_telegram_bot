import asyncio
import logging

from loader import dp, bot, db

async def create_tables():
    sql_cart = """
    CREATE TABLE IF NOT EXISTS cart (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(50),
        product_id INT,
        quantity INT DEFAULT 1,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    );
    """
    sql_orders = """
    CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(50),
        courier_id VARCHAR(50),
        total_price DECIMAL(10,2),
        status VARCHAR(50) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    sql_couriers = """
    CREATE TABLE IF NOT EXISTS couriers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        telegram_id VARCHAR(50) UNIQUE,
        username VARCHAR(100),
        phone VARCHAR(20)
    );
    """
    sql_order_items = """
    CREATE TABLE IF NOT EXISTS order_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        product_id INT,
        quantity INT,
        price DECIMAL(10,2),
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    );
    """
    sql_order_bids = """
    CREATE TABLE IF NOT EXISTS order_bids (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id VARCHAR(50),
        courier_id VARCHAR(50)
    );
    """
    db.execute(sql_cart, commit=True)
    db.execute(sql_couriers, commit=True)
    db.execute(sql_order_bids, commit=True)
    try:
        db.execute("ALTER TABLE orders ADD COLUMN courier_id VARCHAR(50)", commit=True)
    except: pass
    try:
        db.execute("ALTER TABLE orders ADD COLUMN delivery_price DECIMAL(10,2) DEFAULT 0", commit=True)
        db.execute("ALTER TABLE orders ADD COLUMN distance_km DECIMAL(10,2) DEFAULT 0", commit=True)
    except: pass
    db.execute(sql_orders, commit=True)
    db.execute(sql_order_items, commit=True)
    print("Tables created.")
if __name__ == "__main__":
    asyncio.run(create_tables())
