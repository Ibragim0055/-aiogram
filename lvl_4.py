import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, PhotoSize

bot = Bot(token="6047877225:AAFWEU1sb9YUPwylIi5mE-8nL3Od0ic7cuo")
dp = Dispatcher(storage=MemoryStorage())

us = {}

class Photos(StatesGroup):
    a = State()

@dp.message(Command("start"), StateFilter(default_state))
async def start(message: Message, state: FSMContext):
    await message.answer("Жду твоё фото")
    await state.set_state(Photos.a)

@dp.message(StateFilter(Photos.a), F.photo[-1].as_('my_photo'))
async def phot(message: Message, state: FSMContext, my_photo: PhotoSize):
    await state.update_data(photo_unique_id=my_photo.file_unique_id, photo_id=my_photo.file_id)
    us[message.from_user.id] = await state.get_data()
    await message.answer_photo(photo=us[message.from_user.id]['photo_id'])

@dp.message(StateFilter(Photos.a))
async def ph(message: Message):
    await message.answer("ERROR")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())