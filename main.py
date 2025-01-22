import asyncio
from aiogram import Bot,  Dispatcher
from aiogram.types import BotCommand
from config import *
from handlers import *
from middlewares import LoggingMiddleware


# Создаем экземпляры бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.message.middleware(LoggingMiddleware())
dp.include_router(router)



# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())