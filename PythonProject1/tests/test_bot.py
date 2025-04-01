import pytest
from bot import start
from aiogram.types import Message
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock


@pytest_asyncio.fixture
async def mock_message():
    message = AsyncMock(spec=Message)
    message.from_user = MagicMock()
    message.from_user.full_name = 'test user: '
    message.answer = AsyncMock()
    return message


@pytest.mark.acyncio
async def test_start(mock_message):
    await start(mock_message)
    expected_text = f"Вітаю,!\n" "Я перший бот Python розробника Тарнавського Павла."
    mock_message.answer.assert_called_once_with(expected_text)