import os
from typing import Dict

from PyQt5 import QtWidgets
from PyQt5.QtCore import QMimeData
from PyQt5.QtWidgets import QFileDialog, QHeaderView, QMessageBox

from document_processor import read_data, get_common_info, save_changes
from gui.dialog_wrapper import DialogWrapper
from gui.paperlibroutine import Ui_MainWindow
from table_models import FileCheckModel, WorkInfoModel
from pathlib import Path


class Program(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file_selection_model = FileCheckModel()
        self.work_info_model = WorkInfoModel()
        self.common_info = dict.fromkeys((
                                         'teacher', 'teacher_duty', 'topic', 'work_type', 'year', 'group', 'group_code',
                                         'faculty', 'chair', 'chair_short', 'study', 'profile', 'variant',
                                         'discipline_code', 'discipline', 'qual'), str())
        self.common_info['work_type'] = 0

        self.dir_name = str()
        self.setup_widgets()

    def setup_widgets(self):
        """
        Настройка элементов формы
        :return:
        """
        self.ui.edit_path.editingFinished.connect(self.update_filelist)
        self.ui.btn_file_dialog.clicked.connect(self.call_file_dialog)
        self.ui.btn_filelist_refresh.clicked.connect(self.update_filelist)

        self.ui.table_files_view.setModel(self.file_selection_model)
        self.ui.table_files_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.table_files_view.setSortingEnabled(True)
        self.file_selection_model.add_context_menu_actions(self.ui.table_files_view, self.ui.edit_path)

        self.ui.table_students_view.setModel(self.work_info_model)
        self.ui.table_students_view.setSortingEnabled(True)
        # self.ui.table_students_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # self.ui.table_students_view.horizontalHeader().setMaximumWidth(500)
        # @see stackoverflow.com/questions/3433664/how-to-make-sure-columns-in-qtableview-are-resized-to-the-maximum

        # на уровень выше, нужно при работе с файлом перелистывать на начало
        # self.ui.btn_start_reading.clicked.connect(lambda checked, i=1: tab_switch(i))
        self.ui.btn_start_reading.clicked.connect(self.parse_documents)
        self.ui.btn_back_choosing.clicked.connect(self.disable_switch_tab)

        self.ui.btn_change.clicked.connect(self.open_common_info_dialog)
        self.ui.btn_save.clicked.connect(self.save_changes)
        self.ui.btn_clipboard_save.clicked.connect(self.clipboard_copy)
        self.ui.btn_clipboard_open.clicked.connect(self.clipboard_paste)

    def disable_switch_tab(self):
        self.ui.tab_widget.setCurrentIndex(0)
        self.ui.tab_students.setEnabled(False)

    def check_work_existence(self, files):
        return len(files) > 0

    def parse_documents(self):
        """
        Обработка docx документов, нахождение общей информации и ее отображение на второй вкладке
        :return:
        """
        necessary_data = self.file_selection_model.get_data()

        self.file_selection_model.restore_data(necessary_data)

        print('Начинаем чтение')
        files = [file for file, is_checked in necessary_data if is_checked]
        folder = self.ui.edit_path.text()
        result = read_data(folder=folder, files=files)

        if self.check_work_existence(files):
            self.ui.tab_widget.setCurrentIndex(1)  # при переключении вкладки флажки в таблице сбрасываются в False
            self.ui.tab_students.setEnabled(True)

            self.work_info_model.clear()
            self.work_info_model.append(result)

            group_info = get_common_info(result)
            self.render_common_info(group_info)

    def render_common_info(self, new_group_info=dict()) -> Dict[str, str]:
        """
        Формирование информационного сообщения с общей информацией
        :param new_group_info: новая информация, полученная при обработке документов
        :return:
        """
        cache = self.common_info
        if len(new_group_info.items()) > 0:
            teachers = [t for t, works in new_group_info['teacher'] if len(t) > 0]
            topics = [t for t, works in new_group_info['topic'] if len(t) > 0]
            faculties = [t for t, works in new_group_info['faculty'] if len(t) > 0]
            chairs = [t for t, works in new_group_info['chair'] if len(t) > 0]
            groups = [t for t, works in new_group_info['group'] if len(t) > 0]
            group_codes = [t for t, works in new_group_info['group_code'] if len(t) > 0]
            years = [str(t) for t, works in new_group_info['year'] if int(t) > 0]
            work_types = [str(t) for t, works in new_group_info['work_type'] if int(t) >= 0]
            cache['teacher'] = ','.join(teachers)
            cache['topic'] = ','.join(topics)
            cache['faculty'] = ','.join(faculties)
            cache['chair'] = ','.join(chairs)
            cache['group'] = ','.join(groups)
            cache['group_code'] = ','.join(group_codes)
            cache['year'] = ','.join(years)
            cache['work_type'] = ','.join(work_types)

            quals = [t for t, works in new_group_info['qual'] if len(t) > 0]
            disciplines = [t for t, works in new_group_info['discipline'] if len(t) > 0]
            discipline_codes = [t for t, works in new_group_info['discipline_code'] if len(t) > 0]
            profiles = [str(t) for t, works in new_group_info['profile'] if len(t) > 0]
            studies = [str(t) for t, works in new_group_info['study'] if len(t) > 0]
            teacher_duties = [str(t) for t, works in new_group_info['teacher_duty'] if len(t) >= 0]

            cache['qual'] = ','.join(quals)
            cache['discipline'] = ','.join(disciplines)
            cache['discipline_code'] = ','.join(discipline_codes)
            cache['profile'] = ','.join(profiles)
            cache['study'] = ','.join(studies)
            cache['teacher_duty'] = ','.join(teacher_duties)

            self.common_info = cache

        data_desc = 'Преподаватель {teacher_duty} {teacher}\nТема {topic:.50}\n' \
                    'Тип работы {work_type}\nГод {year}\nГруппа {group:.25}\n' \
                    '\nКод группы {group_code}\nФакультет {faculty:.50}\nКафедра {chair:.50}' \
            .format(**cache)
        self.ui.lbl_common_info.setText(data_desc)
        return cache

    def open_common_info_dialog(self):
        change_dialog = DialogWrapper(self)
        change_dialog.set_info(self.common_info)
        change_dialog.show()

        def accept_changes():
            result = change_dialog.get_info()
            self.common_info = change_dialog.get_info()
            self.work_info_model.set_common_data(self.common_info)
            self.render_common_info()
            print(result)

        change_dialog.ui.btn_apply.accepted.connect(accept_changes)

    def update_filelist(self):
        path = self.ui.edit_path.text()
        flag = os.path.exists(path) and os.path.isdir(path)

        print('Путь: {} ({})'.format(path, '+' if flag else '-'))
        if not flag:
            return
        self.dir_name = path

        contents = [item for item in os.listdir(path) if os.path.isfile(os.path.join(path, item))
                    and item.endswith('.docx')]
        self.file_selection_model.clear()
        self.file_selection_model.append(contents)

    def call_file_dialog(self):
        """
        Вызов диалога выбора папки
        :return:
        """
        options = QFileDialog.Options() | QFileDialog.DontUseNativeDialog | \
                  QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks

        home_dir = str(Path.home())
        chosen_dir = self.ui.edit_path.text()
        chosen_dir = chosen_dir if os.path.exists(chosen_dir) and os.path.isdir(chosen_dir) else home_dir

        dir_name = QFileDialog.getExistingDirectory(self, 'Укажите папку с работами', chosen_dir, options=options)

        if dir_name:
            print("Выбрана папка {}".format(dir_name))
            self.ui.edit_path.setText(dir_name)
            self.update_filelist()

    def save_changes(self):
        if len(self.dir_name) == 0 or not os.path.exists(self.dir_name) or not os.path.isdir(self.dir_name):
            QMessageBox.question(self, 'Необходимы дополнительные данные',
                                 'Необходим полный путь к существующей папке', QMessageBox.Apply)
            return

        works = self.work_info_model.get_data()

        title_change_choice = QMessageBox.question(self, 'Скорректировать титульные листы?',
                                                   'Изменить титульные листы в соответствие с данными из таблицы?',
                                                   QMessageBox.Yes | QMessageBox.No)

        save_changes(works, self.common_info, self.dir_name, change_title_pages=title_change_choice == QMessageBox.Yes,
                     call_dialog_method=self.question_rewrite)
        self.work_info_model.clear()
        self.work_info_model.append(works)

    def question_rewrite(self, path, student) -> QMessageBox.StandardButton:
        choice = QMessageBox.question(self, 'Файл с этим именем существует',
                                      "Перезаписать файл {0} с работой \'{1}\'?".format(path, student),
                                      QMessageBox.Yes | QMessageBox.No | QMessageBox.Abort)
        return choice

    def clipboard_copy(self):
        print('Копируем в буфер обмена')
        clipboard_data = self.work_info_model.copy()

        if len(clipboard_data) == 0:
            return

        mime_data = QMimeData()
        mime_data.setText(clipboard_data)
        mime_data.setHtml(clipboard_data)
        app.clipboard().setMimeData(mime_data)

    def clipboard_paste(self):
        mime_data = app.clipboard().mimeData()
        data = mime_data.html() if mime_data.hasHtml() else mime_data.text()
        self.work_info_model.paste(data)

        if len(self.work_info_model.items) > 0:
            group_info = get_common_info(self.work_info_model.items)
            cache = self.render_common_info(group_info)
            self.common_info = cache


if __name__ == "__main__":
    def set_clipboard(clipboard_data: str):
        if not isinstance(clipboard_data, str) or len(clipboard_data) == 0:
            return
        mime_data = QMimeData()
        mime_data.setHtml(clipboard_data)
        app.clipboard().setMimeData(mime_data)


    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Program()
    MainWindow.show()
    sys.exit(app.exec_())
