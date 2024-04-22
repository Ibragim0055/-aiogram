import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import Message

bot = Bot(token="6047877225:AAFWEU1sb9YUPwylIi5mE-8nL3Od0ic7cuo")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    await message.reply("Отправь любое сообщение и я повторю за тобой!")

@dp.message()
async def axo(message: Message):
    a = message.text
    await message.answer(a)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    