from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import auxiliary.messages as messages

def start_keyboard():
    start_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=messages.BUTTON_START)]
        ],
        resize_keyboard=True
    )
    return start_kb

def get_cancel_replay_keyboard():
    cancel_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=messages.BUTTON_CANCEL)]
        ],
        resize_keyboard=True
    )
    return cancel_kb

def user_keyboard():
    user_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=messages.BUTTON_MAKE_APOINT), KeyboardButton(text=messages.BUTTON_ABORTED)]
        ],
        resize_keyboard=True
    )
    return user_kb

def admin_keyboard():
    admin_kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=messages.BUTTON_SLOTS), KeyboardButton(text=messages.BUTTON_ADD), KeyboardButton(text=messages.BUTTON_DEL)],
            [KeyboardButton(text=messages.BUTTON_APOINT)],
        ],
        resize_keyboard=True
    )
    return admin_kb

def get_select_keyboard(items: list | bool, one_time_kb = False):
    builder = ReplyKeyboardBuilder()
    if items:
        for item in items:
            if type(item) == tuple:
                builder.add(KeyboardButton(text=item[0]))
            elif type(item) == str:
                builder.add(KeyboardButton(text=item))
    builder.add(KeyboardButton(text=messages.BUTTON_CANCEL))
    builder.adjust(2)
    select_kb = builder.as_markup(resize_keyboard=True, one_time_keyboard=one_time_kb)
    return select_kb