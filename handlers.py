from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from states import Account, Journal
from requests import get_user, get_subjects, get_students, save_journal, get_subject_by_id, get_journal_by_date
import keyboards
from helpers import validate_date, validate_int, get_ints
import config

router = Router()


async def get_message_actions_with_attendance(message: Message):
    await message.answer(f'Действия с посещаемостью:',
                         reply_markup=keyboards.attendance)


@router.message(CommandStart())
async def start_handler(message: Message):
    """
    Обработчик стартовой команды.
    """
    await message.answer('Привет! Для входа в систему нажми кнопку "Войти"', reply_markup=keyboards.login)


@router.callback_query(F.data == "login")
async def login(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия кнопки "Войти".
    """
    await callback.message.edit_text('Введите свой логин:')
    await state.clear()  # Стираем старые данные пользователя
    await state.set_state(Account.entering_login)  # Устанавливаем состояние ввода логина
    await state.update_data(last_message=callback.message)  # Сохраняем предыдущее сообщение


@router.message(Account.entering_login)
async def login_entered(message: Message, state: FSMContext):
    """
    Обработчик введенного логина.
    """
    user = await get_user(message.text)

    user_data = await state.get_data()
    if user_data['last_message'] is not None:
        await user_data['last_message'].delete()
        await state.update_data(last_message=None)

    if user is None:
        await message.answer(f'Пользователь с логином "{message.text}" не найден', reply_markup=keyboards.login)
    else:
        await message.answer(f'Добро пожаловать, {user.name}!\nВаша группа: {user.group}')
        await get_message_actions_with_attendance(message)
        await state.update_data(user=user)

    await message.delete()
    await state.set_state(Account.logged)


@router.callback_query(Account.logged, F.data == "mark")
async def mark(callback: CallbackQuery, state: FSMContext):
    """
    Отметить посещаемость.
    """
    await callback.message.answer('Введите дату (например: 6.5.2023):')
    await state.set_state(Journal.entering_date)


@router.message(Journal.entering_date)
async def date_entered(message: Message, state: FSMContext):
    """
    Обработчик введенной даты для отметки посещаемости.
    """
    date = validate_date(message.text)

    if date is None:
        await message.answer('Дата введена неверно!')
        await message.answer('Введите дату (например: 6.5.2023):')
    else:
        await state.update_data(date=date)

        # Выводим клавиатуру выбора дисциплины
        subjects = await get_subjects()
        subject_keyboard = keyboards.create_inline_keyboard(config.SUBJECT_PREFIX, subjects)
        await message.answer('Дата записана')
        await message.answer('Выберите дисциплину:', reply_markup=subject_keyboard)
        await state.set_state(Journal.choosing_subject)


@router.callback_query(Journal.choosing_subject, F.data.startswith(config.SUBJECT_PREFIX))
async def subject_entered(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик выбранной дисциплины.
    """
    subject_id = int(callback.data.replace(f'{config.SUBJECT_PREFIX}_', ''))
    await state.update_data(subject_id=subject_id)
    subject = await get_subject_by_id(subject_id)
    await callback.message.answer(f'Выбрана дисциплина "{subject}"')
    await callback.message.answer(f'Введите номер пары в расписании:')
    await state.set_state(Journal.entering_lesson_number)


@router.message(Journal.entering_lesson_number)
async def lesson_number_entered(message: Message, state: FSMContext):
    """
    Обработчик введенного номера пары.
    """
    lesson_number = validate_int(message.text)
    if lesson_number is None:
        await message.answer('Номер пары введен неверно!')
        await message.answer('Введите номер пары в расписании:')
    elif lesson_number <= 0:
        await message.answer('Номер пары должен быть больше нуля!')
        await message.answer('Введите номер пары в расписании:')
    else:
        await state.update_data(lesson_number=lesson_number)
        await message.answer('Номер пары в расписании записан')
        text = 'Введите номера отсутствующих студентов через запятую (например: 1, 6, 9):\n\n'

        # Получаем список студентов
        students = await get_students()
        student_ids = []

        for student in students:
            text += str(student) + '\n'
            student_ids.append(student.id)

        # Сохраняем список выведенных студентов
        await state.update_data(student_ids=student_ids)
        await message.answer(text)

        await state.set_state(Journal.entering_absent_students)


@router.message(Journal.entering_absent_students)
async def absent_students_entered(message: Message, state: FSMContext):
    """
    Обработчик введенных номеров студентов.
    """
    absent_student_ids = get_ints(message.text)
    filtered_absent_student_ids = []
    user_data = await state.get_data()

    if user_data['student_ids'] is not None:
        min_student_id = min(user_data['student_ids'])
        max_student_id = max(user_data['student_ids'])

        for student_id in absent_student_ids:
            if min_student_id <= student_id <= max_student_id:
                filtered_absent_student_ids.append(student_id)
            else:
                await message.answer(f'Номер студента "{student_id}" выходит за границы допустимых!')

    await save_journal(filtered_absent_student_ids, user_data['subject_id'], user_data['user'].id, user_data['date'],
                       user_data['lesson_number'])
    await state.set_state(Account.logged)

    # Сообщение после сохранения посещаемости
    await message.answer('Посещаемость сохранена!')
    await get_message_actions_with_attendance(message)


@router.callback_query(Account.logged, F.data == "view")
async def view(callback: CallbackQuery, state: FSMContext):
    """
    Посмотреть посещаемость.
    """
    await callback.message.answer('Введите дату (например: 6.5.2023):')
    await state.set_state(Journal.entering_date_view)


@router.message(Journal.entering_date_view)
async def date_view_entered(message: Message, state: FSMContext):
    """
    Обработчик введенной даты для просмотра посещаемости.
    """
    date = validate_date(message.text)

    if date is None:
        await message.answer('Дата введена неверно!')
        await message.answer('Введите дату (например: 6.5.2023):')
    else:
        text = f'Посещаемость студентов на {message.text}:'
        journal = await get_journal_by_date(date)

        for item in journal.values():
            text += '\n' + ' '.join(item)

        await message.answer(text)

        # Получаем список предметов
        subjects = await get_subjects()
        subjects = [str(subject) for subject in subjects]

        await message.answer('Описание\n\n3-Н-2 – не было на математике (номер 3) во время 2-ой пары\n\n'
                             'Список всех дисциплин:\n' + '\n'.join(subjects))

        await state.set_state(Account.logged)

        # Сообщение после сохранения посещаемости
        await get_message_actions_with_attendance(message)


@router.message()
async def no_command_handler(message: Message):
    """
    Обработчик несуществующей команды.
    """
    await message.answer('Введенной команды не существует!')
