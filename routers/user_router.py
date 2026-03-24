from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from loguru import logger

import auxiliary.keyboard as kb
import auxiliary.messages as messages
from auxiliary.forms import ApointmentForm
from auxiliary.classes import User, Slot, Apointment

user_router = Router()

reply_markup = kb.user_keyboard()

@user_router.message(F.text.lower() == messages.BUTTON_MAKE_APOINT.lower())
async def apoint(message: Message, state: FSMContext):
    logger.info(f'{messages.USER} {message.from_user.username} {messages.MAKE_RECORD}')

    await state.set_state(ApointmentForm.username)
    await state.update_data(username=message.from_user.username)
    await state.set_state(ApointmentForm.date)

    # Создаем клавиатуру из запроса
    slot = Slot()
    items = await slot.search()
    markup = kb.get_select_keyboard(items)
    await message.answer(f'{messages.SELECT_DATE}', reply_markup=markup)

@user_router.message(F.text.contains('-'), ApointmentForm.date)
async def process_date(message: Message, state: FSMContext):
    slot = Slot(date=message.text)
    times = await slot.search()
    await message.answer(
        f"{messages.YOU_SELECT_DATE} {slot.date}\n{messages.SELECT_TIME}",
        reply_markup=kb.get_select_keyboard(times, True)
    )
    await state.update_data(date=slot.date)
    await state.set_state(ApointmentForm.time)

@user_router.message(F.text.contains(':'), ApointmentForm.time)
async def process_time(message: Message, state: FSMContext, bot: Bot):
    time = message.text
    await message.answer(f'{messages.YOU_SELECT_TIME} {time}')
    await state.update_data(time=time)

    apoint = await state.get_data()
    user = User(username=message.from_user.username)
    user = await user.search()
    slot = Slot(date=apoint['date'], time=apoint['time'])
    apointment = Apointment(slot.date, slot.time, user.userID)

    await apointment.add()
    await slot.delete()

    await message.answer(f'{user.name}, {messages.YOU_ARE_APOINTED_ON} {slot.date} {messages.IN} {slot.time}')
    message = f'{user.name} (@{user.username}) {messages.RECORDED} {slot.date} {messages.IN} {slot.time}'
    logger.info(message)
    await state.clear()
    # admins = await user.get_admins()

@user_router.message(F.text.lower() == messages.BUTTON_ABORTED.lower())
async def aborted(message: Message):
    user = User(username=message.from_user.username)
    user = await user.search()
    apoint = Apointment(userID=user.userID)
    items = await apoint.search_user()
    apoint_list = []
    if items:
        for item in items:
            apoint_list.append(f'{item[0]} {item[1]}')
    markup = kb.get_select_keyboard(apoint_list)
    await message.answer(
        messages.APOINT_LIST,
        reply_markup=markup
    )

@user_router.message(F.text.contains(' '))
async def apoint_del(message: Message):
    dt = message.text.split(' ')
    date = dt[0]
    time = dt[1]
    apoint = Apointment(date, time)
    await apoint.delete()
    slot = Slot(date, time, new=1)
    await slot.add()
    await message.answer(f'{messages.RECORD} {date} {time} {messages.ABORTED}')
    del apoint, slot
