from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

login = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Войти", callback_data="login")]
    ])

attendance = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отметить", callback_data="mark"),
         InlineKeyboardButton(text="Посмотреть", callback_data="view")]
    ])


def create_inline_keyboard(prefix, items) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру в сообщении.
    """
    buttons = [[InlineKeyboardButton(text=f'{item.id}. {item.name}', callback_data=f'{prefix}_{item.id}')] for item in
               items]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
