from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Subject, Student, Journal, Base

# Assuming you have created the tables and connected to the database
engine = create_engine('sqlite:///bot_database.db')
Base.metadata.bind = engine
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Students
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
    "Параллельные времена",
    "Пингвины и звуки",
    "Карамельные частицы",
    "Астрономия для магов",
    "Килты в космосе",
    "Философия котов",
    "Психоанализ роботов",
    "Дома для чувств",
    "Квантовый шоколад",
    "Танцующие листья"
]

subjects = []
for name in subject_names:
    subject = Subject(name=name)
    subjects.append(subject)

session.add_all(subjects)
session.commit()
