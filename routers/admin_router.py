from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from loguru import logger

from auxiliary.classes import User, Slot, Apointment
from auxiliary.forms import DateTimeForm
import auxiliary.db as db
import auxiliary.keyboard as kb
import auxiliary.messages as messages
import auxiliary.checks as check

admin_router = Router()

reply_markup = kb.admin_keyboard()

@admin_router.message(F.text.lower() == messages.BUTTON_SLOTS.lower())
async def get_slots(message: Message):
    slots = await db.get_items('slots')
    if len(slots) == 0:
        await message.answer(messages.NO_SLOTS)
    else:
        text = f'{messages.FREE_SLOTS}\n'
        for slot in slots:
            text = f'{text}{str(slot[1])} {str(slot[2])}\n'
        await message.answer(text)

@admin_router.message(F.text.lower() == messages.BUTTON_ADD.lower())
async def add_slots(message: Message, state: FSMContext):
    logger.info(messages.ADDITION_SLOTS)
    await message.answer(messages.INPUT_DATE_TIME,
                         reply_markup=kb.get_cancel_replay_keyboard()
    )
    await state.set_state(DateTimeForm.date)

@admin_router.message(DateTimeForm.date, F.text.not_contains('-'))
async def proccess_datetime(message: Message, state: FSMContext):
    text = message.text
    tmp = check.date_normalize(text)
    if tmp == None:
        await message.answer(messages.ERROR_REPEAT)
        return
    try:
        dt = datetime.strptime(tmp, '%d.%m.%Y %H:%M')
        slot = Slot()
        slot.date = str(dt.date())
        slot.time = str(dt.time())[:5]
    except:
        await message.answer(messages.ERROR_REPEAT)
        logger.error(messages.ERROR_REPEAT)
        return
    
    apoint = Apointment(date=slot.date, time=slot.time, userID=0)

    if dt < datetime.now():
        await message.answer(messages.ERROR_TIME)
        return
    elif await slot.search() or await apoint.search():
        await message.answer(messages.ERROR_SLOT)
        logger.error(messages.ERROR_SLOT)
        return
    else:
        await state.update_data(date=slot.date)
        await state.set_state(DateTimeForm.time)
        await state.update_data(time=slot.time)
        await slot.add()
        await message.answer(
            f'{messages.SLOT} {slot} {messages.ADD}',
            reply_markup=kb.admin_keyboard()
        )
        del slot

@admin_router.message(F.text.lower() == messages.BUTTON_DEL.lower())
async def del_slot(message: Message, state: FSMContext):
    await state.set_state(DateTimeForm.date)

    # Создаем клавиатуру из запроса
    slot = Slot()
    items = await slot.search()    
    await message.answer(
        messages.SELECT_DATE,
        reply_markup=kb.get_select_keyboard(items)
    )

@admin_router.message(DateTimeForm.date, F.text.contains('-'))
async def process_date(message: Message, state: FSMContext):
    slot = Slot(date=message.text)
    times = await slot.search()
    await message.answer(
        f'{messages.YOU_SELECT_DATE} {slot.date}\n{messages.SELECT_TIME}',
        reply_markup=kb.get_select_keyboard(times)
    )
    await state.update_data(date=slot.date)
    await state.set_state(DateTimeForm.time)

@admin_router.message(DateTimeForm.time, F.text.contains(':'))
async def process_time(message: Message, state: FSMContext):
    slot = Slot(time=message.text)
    apoint = await state.get_data()
    slot.date = apoint['date']
    await message.answer(f'{messages.YOU_SELECT_TIME} {slot.time}')
    await state.update_data(time=slot.time)

    await slot.delete()
    slot.time = '00:00'
    times = await slot.search()
    await message.answer(f'{messages.SLOT} {messages.DEL}',
                        reply_markup=kb.get_select_keyboard(times)
    )

@admin_router.message(F.text.lower() == messages.BUTTON_APOINT.lower())
async def show_apoint(message: Message):
    items = await db.get_items('apointments')
    items_future = []
    for item in items:
        dt = datetime.strptime(f'{item[1]} {item[2]}', '%Y-%m-%d %H:%M')
        if dt > datetime.now():
            items_future.append(item)
    text = f'{messages.FUTURE_APOINT}\n'
    for item in items_future:
        apoint = Apointment(item[1], item[2], item[3])
        user = User()
        user = await user.search(userID=apoint.userID)
        text = f'{text}{apoint.date} {messages.IN} {apoint.time} {messages.RECORDED} ' \
               f'{user.name} (@{user.username}). {messages.TEL} {user.tel}, {messages.EMAIL} {user.email}\n'
        del apoint, user
    await message.answer(text)
    