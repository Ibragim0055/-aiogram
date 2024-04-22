import asyncio 
from aiogram import Bot, Dispatcher, F 
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import PhotoSize, Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup 
import asyncpg
import time
 
 
bot = Bot(token="6047877225:AAFWEU1sb9YUPwylIi5mE-8nL3Od0ic7cuo") 
dp = Dispatcher(storage=MemoryStorage())

class vivod(StatesGroup):
    a = State()
    b = State()


async def cr(): 
    conn = await asyncpg.connect(user='postgres', password='8967824ib', host='localhost', database='ibragim') 
    return conn 
 
 
async def database(): 
    conn = await cr() 
    await conn.execute('''CREATE TABLE IF NOT EXISTS ML_lvl_7 ( 
 id BIGSERIAL PRIMARY KEY, 
 user_id BIGINT, 
 user_name TEXT, 
 balance BIGINT, 
 vklad BIGINT, 
 pribil BIGINT, 
 h BIGINT, 
 m BIGINT, 
 s BIGINT, 
    referrals BIGINT, 
    referrer BIGINT) 
''') 
    await conn.close() 


viv1 = {}

class viv:
    def __init__(self):
        self.summ = None
        self.chet = ""
        self.cuda = ""

 
menu_button = KeyboardButton(text="💼 Профиль")
wallet_button = KeyboardButton(text="💳 Кошелёк")
part_button = KeyboardButton(text="👥 Партнёры")
info_button = KeyboardButton(text="📙 Информация")
calculator_button = KeyboardButton(text="📱 Калькулятор")

menu_key = ReplyKeyboardMarkup(keyboard=[[menu_button], [wallet_button, part_button], [calculator_button, info_button]], resize_keyboard=True, one_time_keyboard=True)

pribils_button = InlineKeyboardButton(text="Собрать прибыль", callback_data="s_p")

sp = InlineKeyboardMarkup(inline_keyboard=[[pribils_button]])

no = KeyboardButton(text="Отменить ❌")

noo = ReplyKeyboardMarkup(keyboard=[[no]], resize_keyboard=True, one_time_keyboard=True)

@dp.message(Command("start")) 
async def start(message: Message): 
    referrer = message.text.split()[1] if len(message.text.split()) > 1 else None 
    conn = await cr() 
    users = await conn.fetchrow('''SELECT * FROM ML_lvl_7 WHERE user_id=$1''', message.from_user.id)
    print(users)
    if users: 
        await menu(message)
    else: 
        if referrer: 
            if int(referrer) != int(message.from_user.id):
                users1 = await conn.fetchrow('''SELECT * FROM ML_lvl_7 WHERE user_id=$1''', int(referrer))
                await conn.execute('''INSERT INTO ML_lvl_7 (user_id, user_name, balance, vklad, pribil, h, m, s, referrer, referrals) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)''', message.from_user.id, message.from_user.username, 0, 0, 0, 0, 0, 0, int(referrer), 0) 
                photos = await bot.get_user_profile_photos(referrer)
                if photos.total_count > 0:
                    await conn.execute('''UPDATE ML_lvl_7 SET referrals = referrals + 1 WHERE user_id=$1''', int(referrer)) 
                    await message.answer_photo(photo=photos.photos[0][0].file_id, caption=f"Вас пригласил <a href='tg://user?id={users1[1]}'> {users1[2]} </a>", parse_mode="HTML")
                    await conn.execute('''UPDATE ML_lvl_7 SET referrals = referrals + 1 WHERE user_id=$1''', int(referrer)) 
                    await bot.send_message(referrer, f"Вы пригласили нового<a href='tg://user?id={message.from_user.id}'> реферала! </a>", parse_mode="HTML") 
                    await menu(message)                
                else:
                    await message.answer(f"Вас пригласил <a href='tg://user?id={users1[1]}'> {users1[2]} </a>", parse_mode="HTML")
                    await conn.execute('''UPDATE ML_lvl_7 SET referrals = referrals + 1 WHERE user_id=$1''', int(referrer)) 
                    await bot.send_message(referrer, f"Вы пригласили нового<a href='tg://user?id={message.from_user.id}'> реферала! </a>", parse_mode="HTML") 
                    await menu(message)
            else:
                await conn.execute('''INSERT INTO ML_lvl_7 (user_id, user_name, balance, vklad, pribil, h, m, s, referrals) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)''', message.from_user.id, message.from_user.username, 0, 0, 0, 0, 0, 0, 0) 
                await message.answer("Вы успешно зарегистрированы")
                await menu(message)
        else: 
            await conn.execute('''INSERT INTO ML_lvl_7 (user_id, user_name, balance, vklad, pribil, h, m, s, referrals) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)''', message.from_user.id, message.from_user.username, 0, 0, 0, 0, 0, 0, 0) 
            await message.answer("Вы успешно зарегистрированы")
            await menu(message)
        
    
    await conn.close()
 

async def menu(message: Message):
    photos = await bot.get_user_profile_photos(message.from_user.id)
    conn = await cr()
    user = await conn.fetchrow('''SELECT * FROM ML_lvl_7 WHERE user_id=$1''', message.from_user.id)
    if photos.total_count > 0:
        await message.answer_photo(photo=photos.photos[0][0].file_id, caption=f"<b>Ваш ID: <code>{user[1]}</code>\n\nВаш вклад: {user[4]}\nВашa прибыль: {user[5]}\n\nВремя до сбора: {user[6]}:{user[7]}:{user[8]}</b>", parse_mode="HTML", reply_markup=sp)
    else:
        await message.answer(f"<b>Ваш ID: <code>{user[1]}</code>\n\nВаш вклад: {user[4]}\nВаш прибыль: {user[5]}\n\nВремя до сбора: {user[6]}:{user[7]}:{user[8]}</b>", parse_mode="HTML", reply_markup=sp)
    await conn.close()
    await message.answer("Главное меню:", reply_markup=menu_key)


@dp.callback_query(F.data == "s_p")
async def sp1(callback: CallbackQuery):
    conn = await cr()
    await conn.execute('''UPDATE ML_lvl_7 SET balance = pribil WHERE user_id=$1''', callback.from_user.id) 
    await conn.execute('''UPDATE ML_lvl_7 SET pribil = 0 WHERE user_id=$1''', callback.from_user.id) 
    await bot.answer_callback_query(callback.id, text="Прибыль успешна собрана")

@dp.callback_query(F.data == "v")
async def v_1(callback: CallbackQuery):
    qiwi =   InlineKeyboardButton(text='Qiwi', callback_data='qiwi1')
    payeer = InlineKeyboardButton(text='Payeer', callback_data='payeer1')
    yandex = InlineKeyboardButton(text='Yandex', callback_data='yandex1')
    viv0 =   InlineKeyboardMarkup(inline_keyboard=[[qiwi], [payeer], [yandex]])
    await callback.message.answer("Выберите способ вывода", reply_markup=viv0)

v_0_1 = False
@dp.callback_query()
async def v_0(callback: CallbackQuery, state: FSMContext):
    global v_0_1
    if callback.data == "qiwi1" and not v_0_1:
        v_0_1 = True
        viv1[callback.from_user.id] = viv()
        viv1[callback.from_user.id].cuda = callback.data
        await callback.message.answer("Введите сумму", reply_markup=noo)
        await state.set_state(vivod.a)
    if callback.data == "payeer1" and not v_0_1:
        v_0_1 = True
        viv1[callback.from_user.id] = viv()
        viv1[callback.from_user.id].cuda = callback.data
        await callback.message.answer("Введите сумму", reply_markup=noo)
        await state.set_state(vivod.a)
    if callback.data == "yandex1" and not v_0_1:
        v_0_1 = True
        viv1[callback.from_user.id] = viv()
        viv1[callback.from_user.id].cuda = callback.data
        await callback.message.answer("Введите сумму", reply_markup=noo)
        await state.set_state(vivod.a)
    v_0_1 = False

@dp.message(F.text.cast(float), StateFilter(vivod.a))
async def v_2(message: Message, state: FSMContext):
    conn = await cr()
    user = await conn.fetchrow('''SELECT * FROM ML_lvl_7 WHERE user_id=$1''', message.from_user.id)
    if user[3] >= float(message.text):
        if float(message.text) >= 10:
            viv1[message.from_user.id].summ = float(message.text)
            await message.answer("Введите номер счёта")
            await state.set_state(vivod.b)
        else:
            await message.answer("Минимальная сумма вывода 10 руб!")
            await state.clear()
    else:
        await message.answer("У вас нету столько на балансе!")
        await state.clear()

@dp.message(StateFilter(vivod.b))
async def v_3(message: Message, state: FSMContext):
    viv1[message.from_user.id].chet = message.text
    await message.answer("Заявка на вывод создана, ожидайте!")
    client = InlineKeyboardButton(text="Выплатить", callback_data="client")
    client1 = InlineKeyboardMarkup(inline_keyboard=[[client]])
    await bot.send_message(1994579994, f"Заявка на вывод:\nсумма: {viv1[message.from_user.id].summ} руб\nсчёт: {viv1[message.from_user.id].chet}\nкуда: {viv1[message.from_user.id].cuda}", reply_markup=client1)
    await state.clear()

@dp.callback_query()
async def cli0(callback: CallbackQuery):
    if callback.data == "client":
        client = InlineKeyboardButton(text="ВЫПЛАЧЕНО", callback_data="client1")
        client1 = InlineKeyboardMarkup(inline_keyboard=[[client]])
        print(callback.message.message_id)
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f"Заявка на вывод:\nсумма: {viv1[callback.from_user.id].summ} руб\nсчёт: {viv1[callback.from_user.id].chet}\nкуда: {viv1[callback.from_user.id].cuda}", reply_markup=client1)

    

@dp.message(F.text == "Отменить ❌")
async def otmen(message: Message):
    await menu(message)


@dp.message(F.text == "💼 Профиль")
async def profil(message: Message):
    await menu(message)

@dp.message(F.text == "💳 Кошелёк")
async def wallet(message: Message):
    wallet_keybord = InlineKeyboardButton(text="Пополнить 📥", callback_data="p")
    wallet1_keybord = InlineKeyboardButton(text="Вывести 📤", callback_data="v")
    wallet1 = InlineKeyboardMarkup(inline_keyboard=[[wallet_keybord, wallet1_keybord]])
    photos = await bot.get_user_profile_photos(message.from_user.id)
    conn = await cr()
    user = await conn.fetchrow('''SELECT * FROM ML_lvl_7 WHERE user_id=$1''', message.from_user.id)
    if photos.total_count > 0:
        await message.answer_photo(photo=photos.photos[0][0].file_id, caption=f"Ваш баланс: {user[3]}", reply_markup=wallet1)
    else:
        await message.answer(f"Ваш баланс: {user[3]}", reply_markup=wallet1)
    await conn.close()





async def main(): 
    await dp.start_polling(bot) 
 
if __name__ == "__main__": 
    asyncio.run(main())