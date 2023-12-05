from aiogram.fsm.state import StatesGroup, State


class Account(StatesGroup):
    entering_login = State()
