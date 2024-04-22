import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

bot = Bot(token="6047877225:AAFWEU1sb9YUPwylIi5mE-8nL3Od0ic7cuo")
dp = Dispatcher(storage=MemoryStorage())

class My(StatesGroup):
    a = State()
    b = State()

user = {}

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Отправь текст SOZ")

@dp.message(F.text.upper() == 'SOZ')
async def soz(message: Message, state: FSMContext):
    await message.answer("Отправь текст")
    await state.set_state(My.a)

@dp.message(StateFilter(My.a), F.text.upper())
async def a1(message: Message, state: FSMContext):
    await state.update_data({"a": message.text})
    await message.answer("Отправь число")
    await state.set_state(My.b)

    

@dp.message(StateFilter(My.a))
async def a2(message: Message):
    await message.answer("Нужен текст!")

@dp.message(StateFilter(My.b), lambda x: x.text.isdigit())
async def b1(message: Message, state: FSMContext):
    await state.update_data({"b": int(message.text)})
    user[message.from_user.id] = await state.get_data()
    await message.answer("YES! /my")
    await state.clear()
    

@dp.message(Command("my"), StateFilter(default_state))
async def myy(message: Message):
    if message.from_user.id in user:
        data = user[message.from_user.id]
        await message.answer(f"a = {data['a']}\nb = {data['b']}")
    else:
        await message.answer("Ты не прошел все шаги!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
