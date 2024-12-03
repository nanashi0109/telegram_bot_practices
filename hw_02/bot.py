import asyncio
from resources.config import TOKEN_2

from aiogram import Bot, Dispatcher

from hw_02.handlers.feedback_handlers import router as start_router


async def main():
    bot = Bot(token=TOKEN_2)
    dispatcher = Dispatcher()

    dispatcher.include_routers(start_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

