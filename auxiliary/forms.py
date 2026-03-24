from aiogram.fsm.state import State, StatesGroup

class UserForm(StatesGroup):
    username = State()
    name = State()
    age = State()
    email = State()
    tel = State()

class DateTimeForm(StatesGroup):
    date = State()
    time = State()

class ApointmentForm(StatesGroup):
    username = State()
    date = State()
    time = State()
