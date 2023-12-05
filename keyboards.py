from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

login = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Войти", callback_data="login")]
    ])

attendance = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отметить", callback_data="mark")],
        [InlineKeyboardButton(text="Посмотреть", callback_data="view")]
    ])
