import time
import pytest
from utils.db_api.db import Database
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def test_db_query_performance():
    db = Database(db_name=DB_NAME, db_user=DB_USER, db_password=DB_PASSWORD, db_host=DB_HOST, db_port=DB_PORT)
    start_time = time.time()
    # Perform a query
    users = db.execute("SELECT * FROM users LIMIT 10", fetchall=True)
    end_time = time.time()
    duration = end_time - start_time
    assert duration < 0.1  # Less than 100ms
    print(f"Query took {duration:.4f} seconds")

def test_bulk_insert_performance():
    db = Database(db_name=DB_NAME, db_user=DB_USER, db_password=DB_PASSWORD, db_host=DB_HOST, db_port=DB_PORT)
    start_time = time.time()
    # Simulate bulk insert - assuming test_table exists or create it
    db.execute("CREATE TABLE IF NOT EXISTS test_perf (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))", commit=True)
    for i in range(100):
        db.execute("INSERT INTO test_perf (name) VALUES (%s)", (f"Test {i}",), commit=True)
    end_time = time.time()
    duration = end_time - start_time
    assert duration < 5.0  # Less than 5 seconds for 100 inserts
    print(f"Bulk insert took {duration:.4f} seconds")
    # Clean up
    db.execute("DROP TABLE test_perf", commit=True)

def test_stress_db():
    db = Database(db_name=DB_NAME, db_user=DB_USER, db_password=DB_PASSWORD, db_host=DB_HOST, db_port=DB_PORT)
    for i in range(1000):
        db.execute("SELECT 1", fetchone=True)
    print("Stress test completed")