from aiogram.fsm.state import StatesGroup, State


class Account(StatesGroup):
    entering_login = State()
    logged = State()


class Journal(StatesGroup):
    entering_date = State()
    entering_date_view = State()
    choosing_subject = State()
    entering_lesson_number = State()
    entering_absent_students = State()
