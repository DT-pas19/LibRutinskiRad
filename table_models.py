import os
import re
from typing import List, Tuple, Dict, Any
from operator import itemgetter
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant, QAbstractItemModel, QMimeData, QSize
from PyQt5.QtWidgets import QAction, QMessageBox, QTableView, QLineEdit, QLabel, QInputDialog
from namedlist import namedlist
from document_structure import Work

__file_check_item__ = namedlist('__file_check_item__', ['check', 'name'])
__file_check_item__.__doc__ = 'Модель выбора файла для таблицы'

__work_info_item__ = namedlist('__work_info_item__', ['name', 'no', 'files', 'topic', 'fac'])
# 'Имя студента', 'Номер', 'Файлы', 'Тема работы', 'Факультет'


class FileCheckModel(QAbstractTableModel):
    def __init__(self):
        self.items = list()
        self.column_captions = ['Учитывать?', 'Наименование']
        super(FileCheckModel, self).__init__()

    def rowCount(self, parent):
        return len(self.items)

    def columnCount(self, parent):
        return len(self.column_captions)

    def data(self, index=QModelIndex(), role: int = Qt.DisplayRole):
        """
        Отображение данных
        :param index: индекс - строка/колонка
        :param role: тип отображения данных
        :return:
        """
        if not index.isValid():
            return QVariant()
        if role == Qt.CheckStateRole and index.column() == 0:
            if self.items[index.row()].check:
                return QVariant(Qt.Checked)
            else:
                return QVariant(Qt.Unchecked)
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return QVariant()
            get_item = itemgetter(index.column())
            return QVariant('{}'.format(get_item(self.items[index.row()])))
        if role == Qt.EditRole:
            get_item = itemgetter(index.column())
            return QVariant('{}'.format(get_item(self.items[index.row()])))
        return QVariant()

    def flags(self, index):
        flag_state = QAbstractItemModel.flags(self, index)
        if index.column() == 0:
            return flag_state | Qt.ItemIsUserCheckable
        else:
            return flag_state

    def headerData(self, column: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        """
        Отображение заголовков
        :param column: номер колонки
        :param orientation: ориентация верт/гориз
        :param role: тип отображения данных
        :return:
        """
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return QVariant(self.column_captions[column])
        return QVariant()

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.DisplayRole):
        if index.column() == 0:
            if isinstance(value, str) and len(value) == 0:
                value = False
            else:
                value = bool(value > 0)
        else:
            value = str(value)
        self.items[index.row()][index.column()] = value
        return True

    def append(self, files: List[str]):
        if not isinstance(files, list) or len(files) == 0 or not all([isinstance(f, str) for f in files]):
            return
        converted_objs = [__file_check_item__(check=False, name=f) for f in files]
        self.items += converted_objs
        self.layoutChanged.emit()

    def clear(self):
        self.items = list()

    def get_data(self) -> Tuple[str, bool]:
        """
        Возвращает представление таблицы в виде массива
        :return: массив кортежей (строка, бул)
        """
        result = [(item.name, item.check) for item in self.items]
        return result

    def restore_data(self, data: Tuple[str, bool]):
        restoration_data = dict(data)
        for i in range(len(self.items)):
            self.items[i].check = restoration_data[self.items[i].name]

    def add_context_menu_actions(self, parent: QTableView, edit_path: QLineEdit):
        parent.setContextMenuPolicy(Qt.ActionsContextMenu)
        select_action = QAction('Выбрать все', self)
        deselect_action = QAction('Снять выделение со всех', self)
        rename_action = QAction('Переименовать', self)
        select_action.triggered.connect(self.select_all)
        deselect_action.triggered.connect(self.deselect_all)
        rename_action.triggered.connect(lambda checked, x=parent, y=edit_path: self.rename_file(x, y))

        parent.addAction(select_action)
        parent.addAction(deselect_action)
        parent.addAction(rename_action)

    def select_all(self):
        """
        Выделение всех элементов
        :return:
        """
        for item in [item for item in self.items if not item[0]]:
            item[0] = True

    def deselect_all(self):
        """
        Снятие выделения со всех элементов
        :return:
        """
        for item in [item for item in self.items if item[0]]:
            item[0] = False

    def rename_file(self, table: QTableView, edit_path: QLineEdit):
        path = edit_path.text()
        existance_check = os.path.exists(path) and os.path.isdir(path)
        if not existance_check:
            QMessageBox.warning(self, 'Необходимы дополнительные данные',
                                 "Указанной папки не существует. Необходим полный путь к существующей папке", QMessageBox.Apply)
            return

        selected_indices = [index.row() for index in table.selectedIndexes()]

        for i in range(len(selected_indices)):
            index = selected_indices[i]
            w = self.items[index]
            old_name = w.name
            blank_space = ' '.join([' ' for i in range(100)])
            new_name, pressed_ok = QInputDialog.getText(table, 'Редактирование имени файла "{2}" ({0}/{1})'.format(i + 1, len(selected_indices), w.name), 'Новое имя файла:' + blank_space, QLineEdit.Normal, w.name)
            if not pressed_ok:
                continue
            if len(new_name) == 0:
                QMessageBox.warning(self, 'Имя файла', 'Была введена пустая строка', QMessageBox.Apply)
                i -= 1
            elif new_name != old_name:
                old_name_full_path = os.path.join(path, old_name)
                new_name_full_path = os.path.join(path, new_name)
                if not os.path.exists(new_name_full_path):
                    self.items[index].name = new_name
                    os.rename(old_name_full_path, new_name_full_path)
                else:
                    QMessageBox.warning(self, 'Существующий файл',
                                        'Файл с именем {} уже существует'.format(new_name), QMessageBox.Apply)
                    i -= 1

    def sort(self, column: int, order: Qt.SortOrder = ...):
        if column == 0:
            return
        self.items = sorted(self.items, key=lambda x: getattr(x, 'name'))
        if order == Qt.DescendingOrder:
            self.items.reverse()
        self.layoutChanged.emit()


class WorkInfoModel(QAbstractTableModel):
    def __init__(self):
        self.items = list()
        self.column_captions = ('Имя', 'Номер', 'Файлы', 'Тип работы', 'Тема работы', 'Вариант', 'Код', 'Дисциплина', 'Год', 'Группа', 'Код группы', 'Факультет', 'Кафедра', 'Руководитель', 'Направление', 'Профиль', 'Квалификация')
        self.column_prop_names = ('student', 'number', 'files', 'work_type', 'topic', 'variant', 'discipline_code', 'discipline', 'year', 'group', 'group_code', 'faculty', 'chair',  'teacher', 'study', 'profile', 'qual')
        super(WorkInfoModel, self).__init__()

    def rowCount(self, parent):
        return len(self.items)

    def columnCount(self, parent):
        return len(self.column_captions)

    def data(self, index=QModelIndex(), role: int = Qt.DisplayRole):
        """
        Отображение данных
        :param index: индекс - строка/колонка
        :param role: тип отображения данных
        :return:
        """
        if not index.isValid():
            return QVariant()
        if role == Qt.DisplayRole or role == Qt.EditRole:
            if self.column_prop_names[index.column()] == 'files':
                file_show_case = ';'.join(self.items[index.row()].files)
                return QVariant(file_show_case)
            get_item = itemgetter(self.column_prop_names[index.column()])
            return QVariant('{}'.format(get_item(self.items[index.row()])))
        return QVariant()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return QAbstractItemModel.flags(self, index) | Qt.ItemIsEditable

    def headerData(self, column: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        """
        Отображение заголовков
        :param column: номер колонки
        :param orientation: ориентация верт/гориз
        :param role: тип отображения данных
        :return:
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.column_captions[column])
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return QVariant(column+1)
        return QVariant()

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.DisplayRole):
        if index.isValid() and role == Qt.EditRole:
            key = self.column_prop_names[index.column()]
            if key == 'files':
                files = value.split(';')
                self.items[index.row()].files = files
                return True
            self.items[index.row()][key] = value
            self.items[index.row()].has_changed = True
            self.dataChanged.emit(index, index)
            return True
        return False

    def set_common_data(self, data: Dict[str, str]):
        attrs = ('topic', 'faculty', 'chair', 'chair_short', 'group', 'group_code', 'teacher', 'work_type', 'year', 'study', 'profile', 'variant', 'discipline_code', 'discipline', 'qual', 'teacher_duty')
        for i in range(len(self.items)):
            for attr in attrs:
                value = data.get(attr, str())
                if value != str() and self.items[i][attr] != value:
                    self.items[i][attr] = value
                    self.items[i].has_changed = True

    def get_data(self) -> List[Work]:
        """
        Возвращает представление таблицы в виде массива
        :return: массив
        """
        return self.items

    def append(self, works: List[Work]):
        if not isinstance(works, list) or len(works) == 0 or not all([isinstance(f, Work) for f in works]):
            return
        self.items += works
        self.layoutChanged.emit()

    def clear(self):
        self.items = list()

    def copy(self) -> str:
        table_headers = [('№', 'Ф.И.О. студента', 'Факультет', 'Код специальности', 'Тема', 'Руководитель', 'Вид работы',
                         'Год защиты', 'Название передаваемых файлов (если файлов несколько, разделять их точкой с запятой)'),
                         ('Должность руководителя', 'Группа', 'Кафедра', 'Сокращ. название кафедры', 'Направление',
                          'Профиль', 'Вариант', 'Код дисциплины', 'Дисциплина', 'Квалификация')]
        table_data = []
        counter = 1
        for item in self.items:
            file_list = ';'.join(item['files'])
            row_visible = [counter, item['student'], item['faculty'], item['group_code'], item['topic'], item['teacher'],
                   item['work_type'], item['year'], file_list]
            row_hidden = [item['teacher_duty'], item['group'], item['chair'], item['chair_short'], item['study'],
                   item['profile'], item['variant'], item['discipline_code'], item['discipline'], item['qual']]
            table_data.append((row_visible, row_hidden))
            counter += 1

        clipboard_data = "<!--StartFragment-->\n"
        clipboard_data += "<table>"

        # <editor-fold desc="Header addition">
        clipboard_data += '<tr>\n'
        for cell in table_headers[0]:  # visible part
            clipboard_data += '\t<th>{}</th>\n'.format(cell)

        clipboard_data += '<!--\n'
        for cell in table_headers[1]:  # hidden part
            clipboard_data += '\t<th>{}</th>\n'.format(cell)
        clipboard_data += '\n-->'

        clipboard_data += '</tr>\n'
        # </editor-fold>

        # <editor-fold desc="Table data addition">
        for row in table_data:
            clipboard_data += '<tr>\n'
            for row_part in range(len(row)):
                if row_part == 1:
                    clipboard_data += '<!--\n'
                for cell in row[row_part]:
                    clipboard_data += '\t<td>{}</td>\n'.format(cell)
                if row_part == 1:
                    clipboard_data += '\n-->'
            clipboard_data += '</tr>\n'
        # </editor-fold>

        clipboard_data += "</table>";
        clipboard_data += "<!--EndFragment-->\n";
        return clipboard_data

    def paste(self, data: str):
        # table_headers = ['№', 'Ф.И.О. студента', 'Факультет', 'Код специальности', 'Тема', 'Руководитель', 'Вид работы',
        #                 'Год защиты', 'Название передаваемых файлов (если файлов несколько, разделять их точкой с запятой)']
        if '<table>' not in data:
            print('В буфере обмена не были найдены необходимые данные')
            return
        result_list = []
        start_point = re.search('</?table>', data).span()[1]
        end_point = re.search('</?table>', data[start_point:]).span()[0]
        table_data = data[start_point:start_point + end_point]

        rows = re.split('</?tr>', table_data)
        rows = list(filter(lambda x: len(x) != 0 and x != '\n', rows))[1:]

        for row in rows:
            if row.strip() == str():
                continue
            row = row.replace('<!--\n', '')
            row = row.replace('\n-->', '')
            cells = re.split('</?td>', row)
            cells = list(filter(lambda x: x != '\n' and x != '\n\t', cells))  # len(x) != 0and

            files = cells[8].split(';')
            common_file_name = os.path.splitext(cells[8])[0]
            number_gr = [part for part in re.split('[_ ]', common_file_name) if part.isnumeric() and len(part) >= 6]
            number = next(iter(number_gr)) if len(number_gr) > 0 else '0'

            work = Work(student=cells[1], number=number, faculty=cells[2], group=(cells[10], cells[3]), topic=cells[4], teacher=cells[5], work_type=cells[6], year=cells[7], files=files,

                        teacher_duty=cells[9], chair=cells[11], chair_short=cells[12], study=cells[13], profile=cells[14], variant=cells[15], discipline=(cells[17], cells[16]), qualification=cells[18])

            result_list.append(work)

        self.clear()
        self.append(result_list)

    def sort(self, column: int, order: Qt.SortOrder = ...):
        if column not in [0, 1, 4, 16]:
            return
        self.items = sorted(self.items, key=itemgetter(self.column_prop_names[column]))
        if order == Qt.DescendingOrder:
            self.items.reverse()
        self.layoutChanged.emit()

#     0           1                   2               3               4               5
# [counter, item['student'], item['faculty'], item['group_code'], item['topic'], item['teacher']
# #         6               7           8
#  item['work_type'], item['year'], file_list]
#
#             9               10              11                  12              13
# [item['teacher_duty'], item['group'], item['chair'], item['chair_short'], item['study'],
#
#         14              15                  16                      17              18
# item['profile'], item['variant'], item['discipline_code'], item['discipline'], item['qual']]
