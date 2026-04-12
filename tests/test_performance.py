import time
import pytest
from utils.db_api.db import Database

def test_db_query_performance():
    db = Database(db_name="t_bot_delivery", db_user="root", db_password="YourPassword", db_host="localhost", db_port=3306)
    start_time = time.time()
    # Perform a query
    users = db.execute("SELECT * FROM users LIMIT 10", fetchall=True)
    end_time = time.time()
    duration = end_time - start_time
    assert duration < 0.1  # Less than 100ms
    print(f"Query took {duration:.4f} seconds")

def test_bulk_insert_performance():
    db = Database(db_name="t_bot_delivery", db_user="root", db_password="YourPassword", db_host="localhost", db_port=3306)
    start_time = time.time()
    # Simulate bulk insert
    for i in range(100):
        db.execute("INSERT INTO test_table (name) VALUES (%s)", (f"Test {i}",))
    end_time = time.time()
    duration = end_time - start_time
    assert duration < 5.0  # Less than 5 seconds for 100 inserts
    print(f"Bulk insert took {duration:.4f} seconds")

# For stress test, perhaps use locust
# But for now, simple loop

def test_stress_db():
    db = Database(db_name="t_bot_delivery", db_user="root", db_password="YourPassword", db_host="localhost", db_port=3306)
    for i in range(1000):
        db.execute("SELECT 1", fetchone=True)
    print("Stress test completed")