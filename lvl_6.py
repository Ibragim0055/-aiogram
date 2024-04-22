import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

bot = Bot(token="6047877225:AAFWEU1sb9YUPwylIi5mE-8nL3Od0ic7cuo")
dp = Dispatcher()

a_b = InlineKeyboardButton(text="ВКЛ", callback_data="a")

keyboard = InlineKeyboardMarkup(inline_keyboard=[[a_b]])

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("ВКЛ", reply_markup=keyboard)

@dp.callback_query(F.data == "a")
async def a_1(callback: CallbackQuery):
    a_b = InlineKeyboardButton(text="ВЫКЛ", callback_data="a1")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[a_b]])
    await callback.message.edit_text(text="ВЫКЛ", reply_markup=keyboard)

@dp.callback_query(F.data == "a1")
async def a_1(callback: CallbackQuery):
    a_b = InlineKeyboardButton(text="ВКЛ", callback_data="a")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[a_b]])
    await callback.message.edit_text(text="ВКЛ", reply_markup=keyboard)
    
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())