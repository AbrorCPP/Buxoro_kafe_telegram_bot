import pytest
from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, User
from unittest.mock import AsyncMock
from handlers.user.user_start import start_cmd
from loader import db

@pytest.fixture
def bot():
    return Bot(token="TEST_TOKEN")

@pytest.fixture
def storage():
    return MemoryStorage()

@pytest.fixture
async def state(storage):
    context = FSMContext(storage=storage, key="test")
    yield context
    await context.clear()

@pytest.mark.asyncio
async def test_start_cmd_new_user(bot, state):
    # Mock message
    message = AsyncMock(spec=Message)
    message.from_user.id = 123456789
    message.from_user.first_name = "Test"
    message.chat.id = 123456789
    message.answer = AsyncMock()

    # Mock db.detect_user to return None
    db.detect_user = AsyncMock(return_value=None)

    await start_cmd(message, state)

    # Check if state is set
    current_state = await state.get_state()
    assert current_state == "UserRegistrationForm:fullname"

    # Check if message was sent
    message.answer.assert_called_once()

# Add more handler tests