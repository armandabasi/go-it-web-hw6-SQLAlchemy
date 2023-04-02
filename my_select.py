from sqlalchemy import func, desc, select, and_, Float

from datebase.db import session
from datebase.models import Teacher, Student, Group, Grade, Subject


def select_1():
    """
    --Знайти 5 студентів із найбільшим середнім балом з усіх предметів.

        SELECT s.full_name_student, ROUND(avg(g.grade), 0) AS avg_grate
        FROM grades g
        LEFT JOIN students s ON s.id = g.student_id
        GROUP BY s.id
        ORDER BY avg_grate DESC
        LIMIT 5;
    :return:
    """
    result = session.query(Student.full_name_student, func.round(func.avg(Grade.grade), 0).label("avg_grate")) \
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc("avg_grate")).limit(5).all()
    return result


def select_2(subject_id):
    """
    -- Знайти студента із найвищим середнім балом з певного предмета.

        SELECT sub.subject, s.full_name_student, ROUND(avg(g.grade), 0) AS avg_grate
        FROM grades g
        LEFT JOIN students s ON s.id = g.student_id
        LEFT JOIN subjects sub ON sub.id = g.subject_id
        WHERE sub.id = 3
        GROUP BY s.id
        ORDER BY avg_grate DESC
        LIMIT 1;
    :return:
    """
    result = result = session.query(
                                    Subject.subject_name,
                                    Student.full_name_student,
                                    func.round(func.avg(Grade.grade), 0).label("avg_grate")) \
                            .select_from(Grade).join(Student).join(Subject)\
                            .filter(Subject.id == subject_id).group_by(Student.id, Subject.subject_name)\
                            .order_by(desc("avg_grate")).limit(1).all()

    return result


def select_3(subject_id):
    """
        -- Знайти середній бал у групах з певного предмета.

        SELECT gr.name_group, sub.subject, ROUND(avg(g.grade), 0) AS avg_grate
        FROM grades g
        LEFT JOIN students s ON s.id = g.student_id
        LEFT JOIN subjects sub ON sub.id = g.subject_id
        LEFT JOIN [groups] gr ON gr.id = s.group_id
        WHERE sub.id = 2
        GROUP BY gr.id
        ORDER BY avg_grate DESC;
    :return:
    """
    result = session.query(
                            Subject.subject_name,
                            Group.name_group,
                            func.round(func.avg(Grade.grade), 0).label("avg_grate")) \
                    .select_from(Grade).join(Student).join(Subject).join(Group) \
                    .filter(Subject.id == subject_id).group_by(Subject.subject_name, Group.name_group) \
                    .order_by(desc("avg_grate")).all()

    return result


def select_4(group_id):
    """
            --Знайти середній бал на потоці (по всій таблиці оцінок)

        SELECT gr.name_group, ROUND(avg(g.grade), 0) AS avg_grate
        FROM grades g
        LEFT JOIN students s ON s.id = g.student_id
        LEFT JOIN [groups] gr ON gr.id = s.group_id
        WHERE gr.id = 3
        GROUP BY gr.id;
    :param group_id:
    :return:
    """
    result = session.query(
                            Group.name_group,
                            func.round(func.avg(Grade.grade), 0).label("avg_grate")) \
                    .select_from(Grade).join(Student).join(Group) \
                    .filter(Group.id == group_id).group_by(Group.id) \
                    .order_by(desc("avg_grate")).all()

    return result


def select_5(teacher_id):
    """
            -- Знайти які курси читає певний викладач.

        SELECT t.id, t.full_name_teacher, s.subject
        FROM subjects s
        LEFT JOIN teachers t ON s.teacher_id = t.id
        WHERE t.id = 5;
    :return:
    """
    result = session.query(
                            Teacher.id,
                            Teacher.fullname,
                            Subject.subject_name) \
                    .select_from(Subject).join(Teacher) \
                    .filter(Teacher.id == teacher_id).all()

    return result


def select_6(group_id):
    """
            -- Знайти список студентів у певній групі

        SELECT g.id, g.name_group, s.full_name_student
        FROM groups g
        LEFT JOIN students s ON s.group_id = g.id
        WHERE g.id = 3;
    :param group_id:
    :return:
    """
    result = session.query(
                            Group.id,
                            Group.name_group,
                            Student.full_name_student) \
                    .select_from(Group).join(Student) \
                    .filter(Group.id == group_id).all()

    return result


def select_7(group_id, subject_id):
    """
            -- Знайти оцінки студентів у окремій групі з певного предмета.

        SELECT gr.name_group, sub.subject, s.full_name_student, g.grade
        FROM grades g
        LEFT JOIN students s ON s.id = g.student_id
        LEFT JOIN [groups] gr ON gr.id = s.group_id
        LEFT JOIN subjects sub ON g.subject_id = sub.id
        WHERE gr.id = 3 AND sub.id = 5;

    :param group_id:
    :param subject_id:
    :return:
    """
    result = session.query(
                            Group.name_group,
                            Subject.subject_name,
                            Student.full_name_student,
                            Grade.grade) \
                    .select_from(Grade).join(Student).join(Group).join(Subject) \
                    .filter(and_(Group.id == group_id, Subject.id == subject_id)).all()

    return result


def select_8(teacher_id):
    """
            -- Знайти середній бал, який ставить певний викладач зі своїх предметів.

        SELECT t.full_name_teacher, ROUND(avg(g.grade),0) AS avg_grate
        FROM grades g
        LEFT JOIN subjects s ON g.subject_id = s.id
        LEFT JOIN teachers t ON t.id = s.teacher_id
        WHERE t.id = 5;
    :param teacher_id:
    :return:
    """
    result = session.query(
                            Teacher.fullname,
                            Subject.subject_name,
                            func.round(func.avg(Grade.grade), 0).label("avg_grate"))\
                    .select_from(Grade).join(Subject).join(Teacher) \
                    .filter(Teacher.id == teacher_id).group_by(Teacher.fullname, Subject.subject_name).all()

    return result


def select_9(student_id):
    """
    -- Знайти список курсів, які відвідує студент.

        SELECT s.full_name_student, sub.subject
        FROM grades g
        LEFT JOIN students s ON s.id = g.student_id
        LEFT JOIN subjects sub ON sub.id = g.subject_id
        WHERE s.id = 12
        GROUP BY sub.id;

    :param student_id:
    :return:
    """
    result = session.query(
                            Student.full_name_student,
                            Subject.subject_name)\
                    .select_from(Grade).join(Student).join(Subject) \
                    .filter(Student.id == student_id).group_by(Student.full_name_student, Subject.subject_name).all()

    return result


def select_10(teacher_id, student_id):
    """
    -- Список курсів, які певному студенту читає певний викладач.

        SELECT t.full_name_teacher, s.full_name_student, sub.subject
        FROM grades g
        LEFT JOIN students s ON s.id = g.student_id
        LEFT JOIN subjects sub ON sub.id = g.subject_id
        LEFT JOIN teachers t ON t.id = sub.teacher_id
        WHERE t.id = 3 AND s.id = 6
        GROUP BY sub.id;
    :param teacher_id:
    :param student_id:
    :return:
    """

    result = session.query(
                            Teacher.fullname,
                            Student.full_name_student,
                            Subject.subject_name)\
                    .select_from(Grade).join(Student).join(Subject).join(Teacher) \
                    .filter(and_(Student.id == student_id, Teacher.id == teacher_id))\
                    .group_by(Teacher.fullname, Student.full_name_student, Subject.subject_name).all()

    return result


def select_11(teacher_id, student_id):
    """
    -- Середній бал, який певний викладач ставить певному студентові

        SELECT t.full_name_teacher, s.full_name_student, ROUND(avg(g.grade), 0) AS avg_grate
        FROM grades g
        LEFT JOIN students s ON s.id = g.student_id
        LEFT JOIN subjects sub ON sub.id = g.subject_id
        LEFT JOIN teachers t ON t.id = sub.teacher_id
        WHERE t.id = 3 AND s.id = 20;
    :param teacher_id:
    :param student_id:
    :return:
    """

    result = session.query(
                            Teacher.fullname,
                            Student.full_name_student,
                            func.round(func.avg(Grade.grade), 0).label("avg_grate"))\
                    .select_from(Grade).join(Student).join(Subject).join(Teacher) \
                    .filter(and_(Student.id == student_id, Teacher.id == teacher_id))\
                    .group_by(Teacher.fullname, Student.full_name_student).all()

    return result


def select_12(group_id, subject_id):
    """
    -- Оцінки студентів у певній групі з певного предмета на останньому занятті.

    :param group_id:
    :param subject_id:
    :return:
    """
    subquery =(select(Grade.date_of)\
                    .join(Student).join(Group)\
                    .filter(and_(Grade.subject_id == subject_id, Group.id == group_id))\
               .order_by(desc(Grade.date_of)).limit(1).scalar_subquery())

    result = session.query(
                            Subject.subject_name,
                            Student.full_name_student,
                            Group.name_group,
                            Grade.grade,
                            Grade.date_of)\
                    .select_from(Grade).join(Student).join(Subject).join(Group) \
                    .filter(and_(Grade.subject_id == subject_id, Group.id == group_id, Grade.date_of == subquery))\
                    .order_by(desc(Grade.date_of)).all()

    return result


if __name__ == '__main__':
    #print(select_1())
    #print(select_2(2))
    #print(select_3(3))
    #print(select_4(3))
    #print(select_5(2))
    #print(select_6(2))
    #print(select_7(2, 5))
    #print(select_8(1))
    #print(select_9(15))
    #print(select_10(1, 5))
    #print(select_11(1, 25))
    print(select_12(2, 5))


