import datetime

from models import User, Subject, Student, Journal, async_session
from sqlalchemy import select


async def get_user(login: str):
    """
    Возвращает пользователя по логину.
    """
    async with async_session() as session:
        result = await session.execute(select(User).where(User.login == login))
        return result.scalars().one_or_none()


async def get_subject_by_id(subject_id: int):
    """
    Возвращает дисциплину по id.
    """
    async with async_session() as session:
        result = await session.execute(select(Subject).where(Subject.id == subject_id))
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


async def save_journal(student_ids: list, subject_id: int, user_id: int, date_attendance: datetime.date,
                       lesson_number: int):
    """
    Сохраняет посещаемость.
    """
    journals = []

    async with async_session() as session:
        result = await session.execute(select(Journal).where(Journal.student_id.in_(student_ids),
                                                             Journal.subject_id == subject_id,
                                                             Journal.user_id == user_id,
                                                             Journal.date_attendance == date_attendance,
                                                             Journal.lesson_number == lesson_number))
        found_student_ids = {item.student_id for item in result.scalars().all()}

        # Добавляем только id, которых нет в бд
        add_student_ids = set(student_ids) - found_student_ids

        for student_id in add_student_ids:
            journal = Journal(student_id=student_id, subject_id=subject_id, user_id=user_id,
                              date_attendance=date_attendance, lesson_number=lesson_number, was_present=True)
            journals.append(journal)

        session.add_all(journals)
        await session.commit()


async def get_journal_by_date(date_attendance: datetime.date) -> dict:
    async with async_session() as session:
        result = await session.execute(select(Journal).where(Journal.date_attendance == date_attendance))
        records = result.scalars().all()
        students = await get_students()
        journal = {student.id: [str(student)] for student in students}

        for record in records:
            journal[record.student_id].append(f'{record.subject_id}-Н-{record.lesson_number}')

        return journal
