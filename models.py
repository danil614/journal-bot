from sqlalchemy import Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
import config
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs

engine = create_async_engine(url=config.DB_URL_ASYNC, echo=True)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True)
    login = mapped_column(String, unique=True)
    group = mapped_column(String)
    name = mapped_column(String)
    # Relationships
    journals = relationship("Journal", back_populates="user")


class Subject(Base):
    __tablename__ = 'subjects'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    # Relationships
    journals = relationship("Journal", back_populates="subject")


class Student(Base):
    __tablename__ = 'students'
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    # Relationships
    journals = relationship("Journal", back_populates="student")


class Journal(Base):
    __tablename__ = 'journals'
    id = mapped_column(Integer, primary_key=True)
    student_id = mapped_column(Integer, ForeignKey('students.id'))
    subject_id = mapped_column(Integer, ForeignKey('subjects.id'))
    user_id = mapped_column(Integer, ForeignKey('users.id'))
    date_attendance = mapped_column(Date)
    lesson_number = mapped_column(Integer)
    was_present = mapped_column(Boolean)
    # Relationships
    student = relationship("Student", back_populates="journals")
    subject = relationship("Subject", back_populates="journals")
    user = relationship("User", back_populates="journals")
