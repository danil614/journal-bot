from aiogram import types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from states import Account, Journal
from requests import get_user, get_subjects, get_students
import keyboards
from helpers import validate_date, validate_int, get_ints
import config

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
    await callback.answer('Введите свой логин:')
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
        await message.answer(f'Добро пожаловать, {user.name}\nВаша группа: {user.group}\n\nПосещаемость:',
                             reply_markup=keyboards.attendance)
        await state.update_data(user=user)

    await message.delete()
    await state.set_state(Account.logged)


@router.callback_query(Account.logged, F.data == "mark")
async def mark(callback: CallbackQuery, state: FSMContext):
    """
    Отметить посещаемость.
    """
    await callback.message.answer('Введите дату (например: 06.05.2023):')
    await state.set_state(Journal.entering_date)


@router.message(Journal.entering_date)
async def date_entered(message: Message, state: FSMContext):
    """
    Обработчик введенной даты.
    """
    date = validate_date(message.text)

    if date is None:
        await message.answer('Дата введена неверно!\nВведите дату (например: 06.05.2023):')
    else:
        await state.update_data(date=date)

        # Выводим клавиатуру выбора дисциплины
        subjects = await get_subjects()
        subject_keyboard = keyboards.create_inline_keyboard(config.SUBJECT_PREFIX, subjects)
        await message.answer('Дата записана\nВыберите дисциплину:', reply_markup=subject_keyboard)
        await state.set_state(Journal.choosing_subject)


@router.callback_query(Journal.choosing_subject, F.data.startswith(config.SUBJECT_PREFIX))
async def subject_entered(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик выбранной дисциплины.
    """
    subject_id = int(callback.data.replace(f'{config.SUBJECT_PREFIX}_', ''))
    await state.update_data(subject_id=subject_id)
    await callback.message.answer('Дисциплина выбрана\nВведите номер пары в расписании:')
    await state.set_state(Journal.entering_lesson_number)


@router.message(Journal.entering_lesson_number)
async def lesson_number_entered(message: Message, state: FSMContext):
    """
    Обработчик введенного номера пары.
    """
    lesson_number = validate_int(message.text)
    if lesson_number is None:
        await message.answer('Номер пары введен неверно!\nВведите номер пары в расписании:')
    else:
        await state.update_data(lesson_number=lesson_number)
        text = 'Номер пары в расписании записан\n\nВведите номера отсутствующих студентов через запятую (например: 1, 6, 9):\n\n'

        # Получаем список студентов
        students = await get_students()
        students = [str(student) for student in students]
        await message.answer(text + "\n".join(students))

        await state.set_state(Journal.entering_absent_students)


@router.message(Journal.entering_absent_students)
async def absent_students_entered(message: Message, state: FSMContext):
    """
    Обработчик введенных номеров студентов.
    """
    absent_student_ids = get_ints(message.text)
    await message.answer(f'"{absent_student_ids}"')


@router.callback_query(Account.logged, F.data == "view")
async def view(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Посмотреть посещаемость')


@router.message()
async def no_command_handler(message: Message, state: FSMContext):
    """
    Обработчик несуществующей команды.
    """
    await message.answer('Введенной команды не существует!')
