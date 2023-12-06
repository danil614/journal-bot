from models import User, Subject, Student, async_session
from sqlalchemy import select


async def get_user(login: str):
    """
    Возвращает пользователя по логину.
    """
    async with async_session() as session:
        result = await session.execute(select(User).where(User.login == login))
        return result.scalars().one_or_none()


async def get_subjects():
    """
    Возвращает список дисциплин.
    """
    async with async_session() as session:
        result = await session.execute(select(Subject))
        return result.scalars().all()


async def get_students():
    """
    Возвращает список студентов.
    """
    async with async_session() as session:
        result = await session.execute(select(Student))
        return result.scalars().all()
