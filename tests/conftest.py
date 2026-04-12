# Pytest configuration
import pytest
from utils.db_api.db import Database

@pytest.fixture(scope="session")
def db():
    # Use test database
    return Database(db_name="test_bot_delivery", db_user="root", db_password="YourPassword", db_host="localhost", db_port=3306)