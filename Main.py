class Student:
    """Класс Student

    Описывает класс студентов, которые могут выставлять лекторам оценки за лекции.

    Attributes
    ----------
    name : str
        имя
    surname : str
        фамилия
    gender : str
        пол
    finished_courses : list
        список завершенных курсов
    courses_in_progress : list
        список курсов в процессе изучения
    grades : dict
        оценки по изучаемым курсам
    instances : list
        список всех экземпляров класса Student

    Methods
    -------
    __init__(name, surname, gender)
        Конструктор класса
    getInstances()
        Возвращает список всех экземпляров класса Student.
    rate_lector(lecturer, course, rating)
        Выставляет оценку лектору по изучаемому курсу.
    average_grade()
        Считает среднюю оценку по всем курсам
    __lt__(other)
        Сравнивает два экземпляра класса Student по средней оценке по всем курсам
    __str__()
        Выводит на экран информацию об экземпляре класса Student в установленном формате
    """

    instances = []

    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.__class__.instances.append(self)

    @classmethod
    def getInstances(cls):
        return cls.instances

    def rate_lector(self, lecturer, course, rating):
        if not isinstance(lecturer, Lecturer):
            print(f'Ошибка: обьект не является лектором')
        elif course not in self.courses_in_progress:
            print(f'Ошибка: студент не изучает {course}')
        elif course not in lecturer.courses_attached:
            print(f'Ошибка: лектор не читает лекции по {course}')
        else:
            if course in lecturer.rating:
                lecturer.rating[course] += [rating]
            else:
                lecturer.rating[course] = [rating]

    def average_grade(self):
        grades_list = []
        for grades in self.grades.values():
            for grade in grades:
                grades_list.append(grade)
        if len(grades_list) > 0:
            return sum(grades_list) / float(len(grades_list))
        else:
            return 'Ошибка: нет оценок'

    def __lt__(self, other):
        """ Return str(self). """
        if not isinstance(other, Student):
            print('Ошибка: сравнение обьектов разных классов не определено')
        else:
            return self.average_grade() < other.average_grade()

    def __str__(self):
        return f"Имя: {self.name}\n" \
               f"Фамилия: {self.surname}\n" \
               f"Средняя оценка за домашние задания: {self.average_grade()}\n" \
               f"Курсы в процессе изучения: {', '.join(map(str, self.courses_in_progress))}\n" \
               f"Завершенные курсы: {', '.join(map(str, self.finished_courses))}\n"


class Mentor:
    """Класс Mentor

    Описывает класс преподавателей.

    Attributes
    ----------
    name : str
        имя
    surname : str
        фамилия
    courses_attached : list
        список закрепленных за преподавателем курсов

    Methods
    -------
    __init__(name, surname)
        Конструктор класса
    """

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    """Класс Lecturer

    Описывает класс лекторов, которые могут получать оценки за лекции.

    Note: Наследник класса Mentor

    Attributes
    ----------
    rating : dict
        оценки за лекции от студентов по читаемым курсам
    instances : list
        список всех экземпляров класса Lecturer

    Methods
    -------
    __init__(name, surname, gender)
        Конструктор класса
    getInstances()
        Возвращает список всех экземпляров класса Lecturer.
    average_rating()
        Считает среднюю оценку за лекции по всем курсам
    __lt__(other)
        Сравнивает два экземпляра класса Lecturer по средней оценке за лекции по всем курсам
    __str__()
        Выводит на экран информацию об экземпляре класса Lecturer в установленном формате
    """

    instances = []

    def __init__(self, name, surname):
        self.rating = {}
        self.__class__.instances.append(self)
        super().__init__(name, surname)

    @classmethod
    def getInstances(cls):
        return cls.instances

    def average_rating(self):
        rating_list = []
        for values in self.rating.values():
            for grade in values:
                rating_list.append(grade)
        if len(rating_list) > 0:
            return sum(rating_list) / float(len(rating_list))
        else:
            return 'Ошибка: нет оценок'

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            print('Not a Student')
        else:
            return self.average_rating() < other.average_rating()

    def __str__(self):
        return f"Имя: {self.name}\n" \
               f"Фамилия: {self.surname}\n" \
               f"Средняя оценка за лекции: {self.average_rating()}\n"


class Reviewer(Mentor):
    """Класс Reviewer

    Описывает класс проверяющих, которые могут выставлять студентам оценки за домашние задания.

    Note: Наследник класса Mentor

    Methods
    -------
    rate_hw(student, course, grade)
        Выставляет студенту оценку за домашние задание по курсу
    __str__()
        Выводит на экран информацию об экземпляре класса Reviewer в установленном формате
    """

    def rate_hw(self, student, course, grade):
        if not isinstance(student, Student):
            print(f'Ошибка: обьект не является студентом')
        elif course not in self.courses_attached:
            print(f'Ошибка: проверяющий не закреплен за курсом {course}')
        elif course not in student.courses_in_progress:
            print(f'Ошибка: студент не изучает {course}')
        else:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]

    def __str__(self):
        return f"Имя: {self.name}\n" \
               f"Фамилия: {self.surname}\n"


def average_grade_by_course(students, course):
    """Вычислит среднюю оценку для списка студентов по заданному курсу.
       Аргументы - список обьектов класса Student и название курса.
       Возвратит строку."""
    all_grades_list = []
    for student in students:
        if course in student.courses_in_progress and course in student.grades.keys():
            for grade in student.grades[course]:
                all_grades_list.append(grade)
    if len(all_grades_list) > 0:
        return f'Средняя оценка за домашние задания по всем студентам ' \
               f'в рамках курса {course}: {sum(all_grades_list) / float(len(all_grades_list))}'
    else:
        return 'Ошибка: оценок еще нет '


def average_rating_by_course(lecturers, course):
    """Вычислит среднюю оценку за лекции для списка лекторов по заданному курсу.
       Аргументы - список обьектов класса Lecturer и название курса.
       Возвратит строку."""
    all_rating_list = []
    for lecturer in lecturers:
        if course in lecturer.courses_attached and course in lecturer.rating.keys():
            for rating in lecturer.rating[course]:
                all_rating_list.append(rating)
    if len(all_rating_list) > 0:
        return f'Средняя оценка за лекции всех лекторов ' \
               f'в рамках курса {course}: {sum(all_rating_list) / float(len(all_rating_list))} '
    else:
        return 'Ошибка: оценок еще нет '
