from itertools import groupby
from operator import itemgetter
from typing import List, Any, Tuple
from docx import Document, text
import re
import os

from namedlist import namedlist

key_words = {'group': 'групп', 'faculty': 'факультет', 'chair': 'кафедра', 'topic': 'на тему', 'student': 'выполнил', 'student_2': 'студент'}


def get_paragraph(key: str, text: List[str], include_next: Tuple[bool, int]=(False, 0)) -> str:
    if key not in key_words or len(text) == 0:
        return str()
    result = [(index, par) for index, par in enumerate(text) if key_words[key] in par.lower()]
    final_result = '\n'.join([r for index, r in result])
    if include_next[0]:
        final_result = ''
        for ind, r in result:
            final_result += r + '\n'
            for i in range(ind + 1, ind + include_next[1] + 1):
                if i < len(text):
                    final_result += text[i] + '\n'
        final_result = final_result.strip()
    return final_result


def remove_keywords(text: str) -> str:
    if len(text) == 0:
        return str()
    key_list = [key for key in key_words.values() if key.lower() in text.lower()]
    reduced_text = text
    split_result = re.split('\w*{0}\w*'.format('\w*|\w*'.join(key_list)), reduced_text, flags=re.IGNORECASE)
    reduced_text = ' '.join(split_result).strip(':()»«"\' \t')
    if '\n' in reduced_text:
        reduced_text.replace('\n', '')
    return reduced_text


def get_bracket_less_line(line: str):
    if '(' in line and ')' in line:
        return line[1:-1]
    return line


def replace_whitespace(line: str):
    if not isinstance(line, str) or len(line) == 0:
        return line
    parts = line.strip().split()
    recombined = ' '.join(parts)
    return recombined


def get_line(substr: str, text: List[str]) -> int:
    if not isinstance(substr, str) or len(substr) == 0:
        return -1
    if not isinstance(text, list) or len(text) == 0:
        return -1
    line_info = [i for i, line in enumerate(text) if replace_whitespace(substr.lower()) in line.lower()]
    line_number = next(iter(line_info))
    return line_number
    # тему работы так он не найдет


def read_data(folder: str, files: List[str]) -> List[Any]:
    full_paths = [os.path.join(folder, file) for file in files]
    existing_ones = list(filter(lambda x: os.path.exists(x), full_paths))
    if len(existing_ones) == 0:
        return

    parsed_info = []
    existing_paths = sorted(existing_ones, key=itemgetter(0))
    for key, documents in groupby(existing_paths, key=lambda x: x[:x.rfind('.')]):
        documents = list(documents)
        if len(documents) == 1:
            doc_path = next(iter(documents))
        elif len(documents) > 1:
            doc_path = next(iter([doc for doc in documents if doc.endswith('.docx')]))

        try:
            document = Document(doc_path)  # 'data/162117_б-МЕТЛипу11_2017_7.docx'
        except:
            print('Ошибка чтения файла')
            continue
        first_page_text = []
        complete_first_page_text = []
        for p in document.paragraphs[:30]:
            complete_first_page_text.append(p.text)
            if len(p.text) > 0:
                first_page_text.append(p.text)

        first_page_text_str = '\n'.join(first_page_text)
        contain_check = [key.lower() in first_page_text_str.lower() for key in key_words.values()]
        if not any(contain_check):
            doc_info = Work(files=documents)
            parsed_info.append(doc_info)
        else:
            faculty_raw = get_paragraph('faculty', first_page_text)
            student_info_raw = get_paragraph('student', first_page_text, include_next=(True, 2))

            student_info_match_ind = re.search('([А-Я][а-я]+ ?){2,5}(([А-Я][а-я]+ ?) ([А-Я][. ]?){2})?', student_info_raw).span()  # search_field
            student_info_raw = student_info_raw[student_info_match_ind[0]:student_info_match_ind[1]]

            topic_raw = get_paragraph('topic', first_page_text, include_next=(True, 2))
            chair_raw = get_paragraph('chair', first_page_text)
            group_raw = get_paragraph('group', first_page_text)

            number_gr = [get_bracket_less_line(sub) for sub in first_page_text_str.split()
                         if get_bracket_less_line(sub).isnumeric() and len(sub) >= 6]
            if len(number_gr) > 0:
                number = next(iter(number_gr))
            else:
                file_name = os.path.split(key)[1]
                number_gr = [part for part in re.split('[_ ]', file_name) if part.isnumeric() and len(part) >= 6]
                number = next(iter(number_gr)) if len(number_gr) > 0 else '0'

            faculty = remove_keywords(faculty_raw)
            chair = remove_keywords(chair_raw)
            topic = remove_keywords(topic_raw)
            group = remove_keywords(group_raw)
            doc_info = Work(student=student_info_raw,
                            number=number, topic=topic, faculty=faculty,
                            chair=chair, group=group, files=documents)
            doc_info['student'] = get_line(student_info_raw, complete_first_page_text)
            doc_info['faculty'] = get_line(faculty, complete_first_page_text)
            doc_info['chair'] = get_line(chair, complete_first_page_text)
            doc_info['topic'] = get_line('на тему:', complete_first_page_text)
            doc_info['group'] = get_line(group, complete_first_page_text)
            doc_info['topic'] = doc_info['topic'] + 1 if doc_info['topic'] != -1 else -1

            parsed_info.append(doc_info)
    # + number of line, where to find, dict + save btn
    print('That array of files was read')
    return parsed_info

        # list(filter(lambda x: len(x) > 0, first_page_text))  # 17-20 первых


class Work(namedlist):
    def __init__(self, student=str(), number=str(), topic=str(), faculty=str(), chair=str(), group=str(), files: List[str] = list()):
        """
        структура работы
        :param student: имя выполнившего
        :param number: номер зачетки
        :param topic: тема
        :param faculty: факультет
        :param chair: кафедра
        :param group: группа
        :param files: файлы
        """
        self.__files__ = list()
        self.student = student
        self.number = number
        self.topic = topic
        self.faculty = faculty
        self.chair = chair
        self.group = group
        self.files = files
        self.lines = {
            'student': 0,
            'number': 0,
            'topic': 0,
            'faculty': 0,
            'chair': 0,
            'group': 0,
        }

    @property
    def files(self) -> List[str]:
        return self.__files__

    @files.setter
    def files(self, value: List[str]):
        if not isinstance(value, list) or not all([isinstance(v, str) for v in value]):
            return
        self.__files__ = value
