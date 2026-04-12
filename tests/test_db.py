import pytest
from utils.db_api.db import Database

# Assuming test database or mock
# For simplicity, use the same DB, but in real, use test DB

@pytest.fixture
def db():
    # Setup test DB
    test_db = Database(db_name="test_bot_delivery", db_user="root", db_password="YourPassword", db_host="localhost", db_port=3306)
    yield test_db
    # Teardown if needed

def test_detect_user(db):
    # Test detecting a user
    user = db.detect_user("123456789")
    assert user is None or isinstance(user, dict)

def test_user_registration(db):
    # Test user registration
    result = db.user_registration("Test User", "123456789", "+998901234567", "40.0,70.0")
    assert result is not None

def test_category_creation(db):
    # Test category creation
    result = db.category_creation("Test Category", "test_image.jpg", "Test description")
    assert result is not None

# Add more tests