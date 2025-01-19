from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
import asyncio


api="***"
bot=Bot(token=api)
dp=Dispatcher(bot,storage=MemoryStorage())
kb_menu=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Расчитать"),
            KeyboardButton(text="info"),
            KeyboardButton(text="Купить")
        ]
    ], resize_keyboard=True
)

kb2=InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')]
    ]
)

kb_product=InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product_A', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product_B', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product_C', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product_D', callback_data='product_buying')]
    ]
)

class UserState(StatesGroup):
    growth=State()
    weight=State()
    age=State()
@dp.message_handler(commands= ["start"])
async def main_start(message):
    await message.answer('Привет! \nВыберите опцию:', reply_markup=kb_menu)

@dp.message_handler(text="Расчитать")
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)

@dp.message_handler(text= "info")
async def get_info(message):
    await message.answer('Этот бот считает каллории для женщин с минимальной физической активностью')

@dp.message_handler(text="Купить")
async def get_buying_list(message):
    await message.answer('Выберите продукт для покупки:')
    with open('A.jpg', "rb") as img_A:
        await message.answer_photo(img_A, 'Название: Product_A | Описание: комплекс A| Цена: 100')
    with open('B.jpg', "rb") as img_B:
        await message.answer_photo(img_B,'Название: Product_B | Описание: комплекс B| Цена: 200')
    with open('C.jpg', "rb") as img_C:
        await message.answer_photo(img_C, 'Название: Product_C | Описание: комплекс C| Цена: 300')
    with open('D.jpg', "rb") as img_D:
        await message.answer_photo(img_D, 'Название: Product_D | Описание: комплекс D| Цена: 400')
    await message.answer('Нажмите на соответствующую кнопку',reply_markup=kb_product)


@dp.callback_query_handler(text= "calories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message,state):

        try:
            a=float(message.text)
            await state.update_data(age=message.text)

            await message.answer('Введите свой рост:')
            await UserState.growth.set()
        except Exception:
            await message.answer('неверный формат возраста')
            await message.answer('Введите свой возраст еще раз:')
            await UserState.age.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message,state):
    try:
        a = float(message.text)
        await state.update_data(growth=message.text)
        await message.answer('Введите свой вес')
        await UserState.weight.set()
    except Exception:
        await message.answer('неверный формат роста')
        await message.answer('Введите свой рост еще раз:')
        await UserState.growth.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    try:
        a = float(message.text)
        await state.update_data(weight=message.text)
        data = await state.get_data()
        k_call=(10*float(data['weight'])+6.25*float(data['growth'])-5*float(data['age'])-161)*1.2
        await message.answer(f'Ваша норма каллорий: {k_call}')
        await state.finish()
    except Exception:
        await message.answer('неверный формат веса')
        await message.answer('Введите свой вес еще раз:')
        await UserState.weight.set()
@dp.callback_query_handler(text= 'product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт')
    await call.answer()


@dp.callback_query_handler(text= 'formulas')
async def get_formulas(call):
    await call.message.answer('call=10*weight(kg)+6.25*growth(cm)-5*age(y)-161)*1.2')
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)