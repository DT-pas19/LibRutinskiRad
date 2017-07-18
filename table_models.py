from typing import List, Tuple, Any
from operator import itemgetter
from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant
from namedlist import namedlist

from document_processor import Work

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

    def data(self, idx=QModelIndex(), role: int = Qt.DisplayRole):
        """
        Отображение данных
        :param idx: индекс - строка/колонка
        :param role: тип отображения данных
        :return:
        """
        if role == Qt.CheckStateRole and idx.column() == 0:
            if self.items[idx.row()].check:
                return QVariant(Qt.Checked)
            else:
                return QVariant(Qt.Unchecked)
        if role == Qt.DisplayRole:
            if idx.column() == 0:
                return QVariant()
            get_item = itemgetter(idx.column())
            return QVariant('{}'.format(get_item(self.items[idx.row()])))
        if role == Qt.EditRole:
            get_item = itemgetter(idx.column())
            return QVariant('{}'.format(get_item(self.items[idx.row()])))
        return QVariant()

    def flags(self, index):
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsUserCheckable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

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

        # имя студента | файл | тема работы | факультет


class WorkInfoModel(QAbstractTableModel):
    def __init__(self):
        self.items = list()
        self.column_captions = ['Имя', 'Номер', 'Тема работы', 'Факультет', 'Кафедра', 'Группа', 'Файлы']
        super(WorkInfoModel, self).__init__()

    def rowCount(self, parent):
        return len(self.items)

    def columnCount(self, parent):
        return len(self.column_captions)

    def data(self, idx=QModelIndex(), role: int = Qt.DisplayRole):
        """
        Отображение данных
        :param idx: индекс - строка/колонка
        :param role: тип отображения данных
        :return:
        """
        if role == Qt.DisplayRole:
            # if idx.column() == 0:
            #    return QVariant()
            get_item = itemgetter(idx.column())
            return QVariant('{}'.format(get_item(self.items[idx.row()])))
        return QVariant()

    def flags(self, index):
        if index.column() == 2:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

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
        return QVariant()

    def setData(self, index: QModelIndex, value: Any, role: int = Qt.DisplayRole):
        self.items[index.row()][index.column()] = value
        return True

    def set_common_data(self):
        pass

    def get_data(self):
        """
        Возвращает представление таблицы в виде массива
        :return: массив
        """
        return self.items

    def append(self, works: List[Work]):
        if not isinstance(works, list) or len(works) == 0 or not all([isinstance(f, Work) for f in works]):
            return
        # converted_objs = [__file_check_item__(check=False, name=f) for f in works]
        self.items += works
        self.layoutChanged.emit()

    def clear(self):
        self.items = list()


