from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    fullname = Column(String, nullable=False)


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name_group = Column(String, nullable=False)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    full_name_student = Column(String, nullable=False)
    group_id = Column(ForeignKey("groups.id", onupdate='CASCADE', ondelete='SET NULL'))
    group = relationship("Group", backref='students')


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    subject_name = Column(String, nullable=False)
    teacher_id = Column(ForeignKey("teachers.id", onupdate='CASCADE', ondelete='SET NULL'))
    teacher = relationship("Teacher", backref='subjects')


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grade = Column(Integer, nullable=False)
    date_of = Column(Date, nullable=False)
    subject_id = Column(ForeignKey("subjects.id", onupdate='CASCADE', ondelete='SET NULL'))
    student_id = Column(ForeignKey("students.id", onupdate='CASCADE', ondelete='SET NULL'))
    subject = relationship("Subject", backref='grades')
    student = relationship("Student", backref='grades')


