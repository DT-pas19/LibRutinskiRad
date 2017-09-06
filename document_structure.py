from typing import List, Dict, Tuple
from _datetime import datetime


class Work(dict):
    def __init__(self, student=str(), number=str(), qualification='бакалавр', topic=str(), faculty=str(), chair=str(), chair_short=str(), group: Tuple[str, str] = ('', ''), year=datetime.now().year, work_type=5, teacher=str(), teacher_duty=str(), study=str(), profile=str(), variant=str(), discipline: Tuple[str, str] = ('', ''), files: List[str] = list()):
        """
        структура работы
        :param student: имя выполнившего
        :param number: номер зачетки
        :param topic: тема
        :param faculty: факультет
        :param chair: кафедра
        :param group: группа и код группы
        :param work_type: группа
        :param files: файлы
        :param qualification: квалификация (бакалавр/магистр)
        :param discipline: дисциплина (название+код Бx.x.x)
        :param variant: вариант
        :param study: направление обучения
        :param profile: профиль обучения
        :param teacher: руководитель-преподаватель
        :param year: год сдачи/защиты работы
        """
        default_values = dict(zip(('student', 'number', 'topic', 'faculty', 'chair', 'group', 'group_code', 'year', 'work_type', 'teacher', 'study', 'profile', 'variant', 'discipline', 'discipline_code', 'qual', 'teacher_duty', 'chair_short'), (student, number, topic, faculty, chair, group[0], group[1], year, work_type, teacher, study, profile, variant, discipline[0], discipline[1], qualification, teacher_duty, chair_short)))
        for k, v in default_values.items():
            self[k] = v

        self.files = files
        self.lines = {
            'student': 0,
            'number': 0,
            'topic': 0,
            'faculty': 0,
            'chair': 0,
            'group': 0,
            'year': 0,
        }
        self.has_changed = False

    @property
    def files(self) -> List[str]:
        return self.get('files', str())

    @files.setter
    def files(self, value: List[str]):
        if not isinstance(value, list) or not all([isinstance(v, str) for v in value]):
            return
        self['files'] = value
