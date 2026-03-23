import asyncio
import logging

from loader import dp, bot
from handlers.user_start import router


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    dp.include_router(router=router)
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
