from aiogram import Dispatcher,filters,Bot,F
from aiogram.types import(
    ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton,
    CallbackQuery,Message,BotCommand
)
from db import Users,Questions,Quizzes,Options,engine
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup,State
from sqlalchemy.orm import sessionmaker
Session=sessionmaker(bind=engine)
session=Session()
from datetime import datetime
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
Token=os.getenv('Token')

dp=Dispatcher()

comand=[
    BotCommand(command='start', description='start bot')
]


class Wait(StatesGroup):
    wait_for_test_name=State()
    wait_for_test_description=State()
    wait_for_question=State()
    wait_for_options=State()
    wait_for_correct_option=State()

@dp.message(filters.Command('start'))
async def start_bot(message:Message):
    us=session.query(Users).filter_by(tg_id=message.from_user.id).first()
    if not us:
        tg_id=message.from_user.id
        language=message.from_user.language_code
        name=message.from_user.username
        user=Users(
            tg_id=tg_id,
            language=language,
            name=name
        )
        session.add(user)
        session.commit()
    markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Создать новый тест",callback_data='cnt')],
            [InlineKeyboardButton(text="Мои тесты",callback_data='mt')],
            [InlineKeyboardButton(text="Язык", callback_data='ln')],
        ]
    )
    await message.answer(text='С помощью этого бота Вы можете создать тест из нескольких вопросов с правильными ответами.',reply_markup=markup)

@dp.callback_query(F.data=='cnt')
async def create_test(call:CallbackQuery,state:FSMContext):
    await call.message.answer('Вы решили создать новый тест. Для начала, пожалуйста, пришлите название Вашего теста (например, «Тест на знание математики» или «10 вопросов о Великой Французской Буржуазной Революции»).')
    await state.set_state(Wait.wait_for_test_name)

@dp.message(Wait.wait_for_test_name)
async def cont(message:Message,state:FSMContext):
    await state.update_data(test_name=message.text)
    await message.answer('Пожалуйста, пришлите описание для Вашего теста.')
    await state.set_state(Wait.wait_for_test_description)

@dp.message(Wait.wait_for_test_description)
async def desc(message:Message,state:FSMContext):
    await state.update_data(test_desc=message.text)
 
    data=await state.get_data()
    user=session.query(Users).filter_by(tg_id=message.from_user.id).first()
    name=Quizzes(
        creator_id=user.id,
        title=data['test_name'],
        description=data['test_desc'],
    )
    session.add(name)
    session.commit()
   
    markup=ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Создать вопрос')]
        ],
        resize_keyboard=True
    )
    await message.answer(text=''''Отправьте мне первый вопрос Вашего теста в виде опроса с вариантами ответа. Вы также можете отправить сообщение с текстом или медиа, которое будет показываться перед вопросом.
    Важно: этот бот не может создавать анонимные опросы. При прохождении теста в группах, их участники всегда будут видеть, кто голосовал за какой вариант.''',reply_markup=markup)
    await state.clear()

@dp.message(F.text=='Создать вопрос')
async def create_quize()

async def main():
    bot=Bot(token=Token)
    await bot.set_my_commands(comand)
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())