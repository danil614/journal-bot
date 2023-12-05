from models import User, async_session
from sqlalchemy import select


async def get_user(login: str):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.login == login))
        return result.scalars().one_or_none()
