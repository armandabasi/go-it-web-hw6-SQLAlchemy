from datetime import datetime, date, timedelta
from random import randint, choice
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError

from datebase.db import session
from datebase.models import Teacher, Student, Group, Grade, Subject

from faker import Faker

fake = Faker("uk-UA")

subjects = [
    "Математичні задачі енергетики",
    "Електричні мережі ",
    "Математичні моделі електричних систем",
    "Методи оптимізації режимів енергосистем ",
    "Регулювання режимів електричних систем",
    "Теорія автоматичного керування",
    "Моделі оптимального розвитку енергосистем"
]

groups = [
    "EC-91",
    "EK-91",
    "EM-91"
]

NUMBERS_TEACHERS = randint(3, 5)
NUMBERS_STUDENTS = randint(30, 50)


def reset_autoincrement(table_name):
    session.execute(text(f"TRUNCATE {table_name} RESTART IDENTITY CASCADE"))


def get_period():
    start_of_studies = datetime.strptime("2022-09-01", "%Y-%m-%d")
    end_of_studies = datetime.strptime("2023-06-30", "%Y-%m-%d")

    def get_list_of_date(start_of_studies, end_of_studies):
        result = []
        current_date = start_of_studies
        while current_date <= end_of_studies:
            if current_date.isoweekday() < 6:
                result.append(current_date)
            current_date += timedelta(1)
        return result

    list_dates = get_list_of_date(start_of_studies, end_of_studies)
    return list_dates


def create_teachers():
    reset_autoincrement('teachers')
    session.query(Teacher).delete()
    for _ in range(NUMBERS_TEACHERS):
        teacher = Teacher(
            fullname=fake.name()
        )
        session.add(teacher)
    session.commit()


def create_groups():
    reset_autoincrement('groups')
    session.query(Group).delete()
    for group in groups:
        session.add(Group(name_group=group))
    session.commit()


def create_subjects():
    reset_autoincrement('subjects')
    session.query(Subject).delete()
    list_teachers_id = session.scalars(select(Teacher.id)).all()
    for subject in subjects:
        session.add(Subject(subject_name=subject, teacher_id=choice(list_teachers_id)))
    session.commit()


def create_students():
    reset_autoincrement('students')
    session.query(Student).delete()
    list_group_id = session.scalars(select(Group.id)).all()
    for _ in range(NUMBERS_STUDENTS):
        session.add(Student(full_name_student=fake.name(), group_id=choice(list_group_id)))
    session.commit()


def create_grades():
    reset_autoincrement('grades')
    session.query(Grade).delete()
    list_dates = get_period()
    for student in range(1, NUMBERS_STUDENTS):
        for _ in range(randint(1, 20)):
            random_subject = session.scalars(select(Subject.id)).all()
            random_day = list_dates[randint(1, len(list_dates)-1)].date()
            grade = Grade(
                grade=randint(1, 100),
                date_of=random_day,
                subject_id=choice(random_subject),
                student_id=student
            )
            session.add(grade)
    session.commit()


if __name__ == "__main__":
    try:
        create_teachers()
        create_groups()
        create_subjects()
        create_students()
        create_grades()

    except SQLAlchemyError as e:
        session.rollback()
        print(e)
    finally:
        session.close()

