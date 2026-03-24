from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from loguru import logger

from auxiliary.forms import UserForm
from auxiliary.classes import User
import auxiliary.keyboard as kb
import auxiliary.messages as messages

start_router = Router()

@start_router.message(Command('cancel'))
@start_router.message(F.text.lower() == messages.BUTTON_CANCEL.lower())
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    user = User(username=message.from_user.username)
    user = await user.search()
    if user.isAdmin:
        await message.answer(
            f'{messages.SELECT_ACTION}',
            reply_markup=kb.admin_keyboard()
        )
    else:
        await message.answer(
            f'{messages.SELECT_ACTION}',
            reply_markup=kb.user_keyboard()
        )
    logger.info(messages.INPUT_CANCELED)


@start_router.message(Command('start'))
@start_router.message(F.text.lower() == messages.BUTTON_START.lower())
async def start(message: Message, state: FSMContext):
    user = User(username=message.from_user.username)
    await state.update_data(username=user.username)
    if not await user.search():
        logger.info(f'{user.username} {messages.FILLS_FORM}')
        await message.answer(
            f'{messages.FILLS_FORM_START}\n{messages.FILLS_FORM_NAME}',
            reply_markup=kb.get_cancel_replay_keyboard()
            )
        del user
        await state.set_state(UserForm.name)

    else:
        logger.info(f'{message.from_user.username} {messages.IN_DB}')
        if user.isAdmin:
            await message.answer(
                f'{messages.SELECT_ACTION}',
                reply_markup=kb.admin_keyboard()
            )
        else:
            await message.answer(
                f'{messages.SELECT_ACTION}',
                reply_markup=kb.user_keyboard()
            )
