import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

bot = Bot(token="6047877225:AAFWEU1sb9YUPwylIi5mE-8nL3Od0ic7cuo")
dp = Dispatcher()

a = KeyboardButton(text="my id")
b = KeyboardButton(text="my username")
c = KeyboardButton(text="my photo")

keyboard = ReplyKeyboardMarkup(keyboard=[[a], [b, c]], resize_keyboard=True, one_time_keyboard=True)

us = {}

class UserData:
    def __init__(self):
        self.id = 0
        self.user_name = ""
        self.photos = []

@dp.message(Command("start"))
async def start(message: Message):
    us[message.from_user.id] = UserData()
    us[message.from_user.id].id = message.from_user.id
    us[message.from_user.id].user_name = message.from_user.username
    us[message.from_user.id].photos = await bot.get_user_profile_photos(message.from_user.id)
    await message.answer("Выберите:", reply_markup=keyboard)

@dp.message(F.text == 'my id')
async def a1(message: Message):
    try:
        await message.answer(f"YOUR ID: {us[message.from_user.id].id}", reply_markup=keyboard)
        await bot.send_message(1994579994, f"YOUR ID: {us[message.from_user.id].id}", reply_markup=keyboard)
    except:
        await message.answer("/start")

@dp.message(F.text == 'my username')
async def a2(message: Message):
    try:
        await message.answer(f"YOUR USERNAME: {us[message.from_user.id].user_name}", reply_markup=keyboard)
        await bot.send_message(1994579994, f"YOUR USERNAME: {us[message.from_user.id].user_name}", reply_markup=keyboard)
    except:
        await message.answer("/start")

@dp.message(F.text == 'my photo')
async def a3(message: Message):
    try:
        photos = us[message.from_user.id].photos
        if photos.total_count > 0:
            await message.answer_photo(photo=photos.photos[0][0].file_id, text="YOUR PHOTO", reply_markup=keyboard)
            await bot.send_photo(1994579994, photo=photos.photos[0][0].file_id, text="YOUR PHOTO", reply_markup=keyboard)
        else:
            await message.answer("Нет фото")
    except:
        await message.answer("/start")
    

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
