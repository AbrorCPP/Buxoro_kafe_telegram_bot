import asyncio
import logging

from loader import dp, bot
from router import router
import handlers.user
import handlers.super_admin
import handlers.courier
from aiogram.types import Message

@router.message()
async def cleanup_unhandled_messages(message: Message):
    """
    Deletes any messages that were not caught by existing handlers
    to keep the chat UI extremely clean.
    """
    try:
        await message.delete()
    except:
        pass

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    dp.include_router(router=router)
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
