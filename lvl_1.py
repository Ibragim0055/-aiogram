import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import Message

bot = Bot(token="6047877225:AAFWEU1sb9YUPwylIi5mE-8nL3Od0ic7cuo")

dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello!")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())