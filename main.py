import asyncio
import logging
from aiogram import Bot, Dispatcher, types
# from aiogram.utils.keyboard import InlineKeyboardBuilder
#
# from sqlalchemy import create_engine
# from models import User, Subject, Student, Journal, Base
# from sqlalchemy.orm import Session
#
# engine = create_engine('sqlite:///bot_database.db')

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token='')
# Диспетчер
dp = Dispatcher()


# @dp.message(commands=["start"])
# async def start(message: types.Message):
#     # builder = InlineKeyboardBuilder()
#     # builder.add(types.InlineKeyboardButton(
#     #     text="Войти",
#     #     callback_data="login")
#     # )
#     #
#     # await message.answer(
#     #     "Нажмите кнопку, чтобы войти:",
#     #     reply_markup=builder.as_markup()
#     # )
#     await message.reply("Привет!\nЯ Эхо-бот от Skillbox!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")
@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

# @dp.callback_query(text="login")
# async def send_random_value(callback: types.CallbackQuery):
#     await callback.message.answer("Введите ваш логин:")
#
#
# @dp.message(lambda message: message.text)
# async def process_login(message: types.Message):
#     session = Session()
#     user = session.query(User).filter_by(username=message.text).first()
#     if user:
#         await message.reply("Вы успешно вошли!" + " " + user.name)
#     else:
#         await message.reply("Пользователь не найден. Попробуйте еще раз.")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
