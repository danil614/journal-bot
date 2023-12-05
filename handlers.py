from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from states import Account
from requests import get_user
import keyboards

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    """
    Обработчик стартовой команды.
    """
    await message.answer('Привет! Для входа в систему нажми кнопку "Войти"', reply_markup=keyboards.login)


@router.callback_query(F.data == "login")
async def login(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия кнопки "Войти".
    """
    await callback.answer('Введи свой логин:')
    await state.update_data(user=None)  # Стираем старые данные пользователя
    await state.set_state(Account.entering_login)  # Устанавливаем состояние ввода логина


@router.message(Account.entering_login)
async def login_entered(message: Message, state: FSMContext):
    """
    Обработчик введенного логина.
    """
    user = await get_user(message.text)

    if user is None:
        await message.answer(f'Пользователь с логином "{message.text}" не найден', reply_markup=keyboards.login)
    else:
        await message.answer(f'ФИО: {user.name}\nГруппа: {user.group}\n\nПосещаемость:',
                             reply_markup=keyboards.attendance)
        await state.update_data(user=user)

    await message.delete()
    await state.clear()


@router.callback_query(F.data == "view")
async def view(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Просмотреть посещаемость')


@router.callback_query(F.data == "mark")
async def view(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Отметить посещаемость')
