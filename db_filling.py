from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import User, Subject, Student, Journal, Base
import config


def fill_database():
    engine = create_engine(config.DB_URL)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        student_names = [
            "Белов Даниил Алексеевич",
            "Иванова Александра Дмитриевна",
            "Карпов Артемий Петрович",
            "Козлова Анастасия Владимировна",
            "Коновалов Николай Артемович",
            "Михайлова Ольга Ивановна",
            "Морозов Илья Павлович",
            "Николаева Елизавета Васильевна",
            "Павлова Арина Григорьевна",
            "Петров Никита Сергеевич",
            "Сидорова Алина Максимовна",
            "Смирнова Мария Ивановна",
            "Соколов Владислав Игоревич",
            "Степанова Виктория Юрьевна",
            "Титов Фёдор Владимирович",
            "Федоров Егор Александрович",
            "Федорова Валерия Алексеевна",
            "Хохлов Андрей Петрович",
            "Чернова Екатерина Степановна",
            "Шестакова Анна Алексеевна"
        ]

        students = []
        for name in student_names:
            student = Student(name=name)
            students.append(student)

        session.add_all(students)
        session.commit()

        subject_names = [
            "История",
            "Информатика",
            "Математика",
            "Экология",
            "Политология",
            "Правоведение",
            "Теория управления",
            "Прогнозирование и планирование",
            "Психология",
            "Основы элитологии"
        ]

        subjects = []
        for name in subject_names:
            subject = Subject(name=name)
            subjects.append(subject)

        session.add_all(subjects)
        session.commit()

        insert_users(session)


def insert_users(session):
    users = [User(login="Name", group="GroupTest", name="Test Name One"),
             User(login="Test", group="TEST-4", name="Тестовый Тест Тестович")]
    session.add_all(users)
    session.commit()


if __name__ == "__main__":
    fill_database()
