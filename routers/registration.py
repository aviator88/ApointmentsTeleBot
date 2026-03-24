from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from loguru import logger

from auxiliary.forms import UserForm
from auxiliary.checks import strIsEmail, strIsTel
from auxiliary.classes import User
import auxiliary.db as db
import auxiliary.keyboard as kb
import auxiliary.messages as messages


registration = Router()

@registration.message(Command('cancel'))
@registration.message(F.text.lower() == messages.BUTTON_CANCEL)
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'{messages.INPUT_CANCELED}')
    logger.info(f'{messages.INPUT_CANCELED}')

@registration.message(UserForm.name, F.text)
async def proccess_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        f'{messages.GREAT}\n{messages.INPUT_AGE}',
        reply_markup=kb.get_cancel_replay_keyboard()
        )
    await state.set_state(UserForm.age)

@registration.message(UserForm.age, F.text)
async def proccess_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(f'{messages.AGE_MUST_NUMBER}')
        return   
    elif int(message.text) < 1 or int(message.text) > 100:
        await message.answer(f'{messages.AGE_MUST_1_100}')
        return
    else:
        await state.update_data(age=int(message.text))
        await message.answer(
            f'{messages.GREAT}\n{messages.INPUT_EMAIL}',
            reply_markup=kb.get_cancel_replay_keyboard()
            )
        await state.set_state(UserForm.email)

@registration.message(UserForm.email, F.text)
async def proccess_email(message: Message, state: FSMContext):
    email_text = message.text
    email_text = email_text.lower()
    logger.info(f'{messages.CHECK_EMAIL} {email_text}')
    isEmail = strIsEmail(email_text)
    if isEmail == 0:
        await message.answer(
            f'{messages.EMAIL_CORRECT} {messages.INPUT_TEL}',
            reply_markup=kb.get_cancel_replay_keyboard()
        )
        logger.error(messages.EMAIL_CORRECT)
        await state.update_data(email=message.text)
        await state.set_state(UserForm.tel)
    else:
        await message.answer(f'{messages.EMAIL_UNCORRECT}')
        logger.error(messages.EMAIL_UNCORRECT)
        return
    
@registration.message(UserForm.tel, F.text)
async def proccess_tel(message: Message, state: FSMContext):
    logger.info(f'{messages.CHECK_TEL} {message.text}')
    if message.text[0] == '+':
        tel_text = message.text[1:]
    else:
        tel_text = message.text
    
    isTel = strIsTel(tel_text)

    if isTel == 0:
        await message.answer(f'{messages.TEL_CORRECT}')
        logger.error(messages.TEL_CORRECT)
        await state.update_data(tel=message.text)
    else:
        await message.answer(f'{messages.TEL_UNCORRECT}')
        logger.error(messages.TEL_UNCORRECT)
        return

    data = await state.get_data()
    new_user = User(message.from_user.username)
    new_user.name = data['name']
    new_user.age = data['age']
    new_user.email = data['email']
    new_user.tel = data['tel']
    new_user.isAdmin = False
    if len(await db.get_items('users')) == 0:
        new_user.isAdmin = True

    logger.info(f'{messages.QUSTIONNAIRE_FILLED}: ' \
                f'{messages.NICKNAME}: {new_user.username}, ' \
                f'{messages.NAME}: {new_user.name}, ' \
                f'{messages.AGE}: {new_user.age}, ' \
                f'{messages.EMAIL}: {new_user.email}, '\
                f'{messages.TEL}: {new_user.tel}')
    await message.answer(f'{messages.QUSTIONNAIRE_FILLED}')
    await new_user.add()

    await state.clear()