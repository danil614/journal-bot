from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    group = Column(String)
    name = Column(String)
    # Relationships
    journals = relationship("Journal", back_populates="user")


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Relationships
    journals = relationship("Journal", back_populates="subject")


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Relationships
    journals = relationship("Journal", back_populates="student")


class Journal(Base):
    __tablename__ = 'journals'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    date_attendance = Column(Date)
    lesson_number = Column(Integer)
    was_present = Column(Boolean)
    # Relationships
    student = relationship("Student", back_populates="journals")
    subject = relationship("Subject", back_populates="journals")
    user = relationship("User", back_populates="journals")
