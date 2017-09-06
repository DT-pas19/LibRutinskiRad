from typing import Optional, Dict
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget

from gui.common_options_dialog import Ui_Dialog
from gui.paperlibroutine import Ui_MainWindow
from table_models import WorkInfoModel


class DialogWrapper(QtWidgets.QDialog):
    def __init__(self, MainWindow: Optional[QWidget]):
        super().__init__(MainWindow)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setup_widgets()
        self.__keys__ = ('teacher', 'topic', 'work_type', 'year', 'group', 'group_code', 'faculty')

    def setup_widgets(self):
        self.ui.box_work_type.addItems(['1. Выпускная квалификационная работа',
                                        '2. Дипломная работа',
                                        '3. Дипломный проект',
                                        '4. Магистерская диссертация',
                                        '5. Отчет по практике',
                                        '6. Курсовой проект',
                                        '7. Контрольная работа',
                                        '8. Расчетно-графическая работа',
                                        '9. Курсовая работа',
                                        '10. Научная квалификационная работа',
                                        '11. Научный доклад'])

        # self.ui.btn_apply.accepted.connect(self.accept_changes)
        # list_type_index = self.ui.list_dropdown_box.currentIndex()

    def set_info(self, data: Dict[str, str]):
        if not isinstance(data, dict) or not any(key in data.keys() for key in self.__keys__):
            return

        def exists(key: str):
            return key in data.keys() and data.get(key, None) is not None
        if exists('teacher'):
            self.ui.edit_teacher.setText(data['teacher'])
        if exists('teacher_duty'):
            self.ui.edit_teacher_duty.setText(data['teacher_duty'])
        if exists('topic'):
            self.ui.edit_topic.setText(data['topic'])
        if exists('work_type'):
            self.ui.box_work_type.setCurrentIndex(int(data['work_type']) - 1)
        if exists('year'):
            self.ui.edit_year.setText(data['year'])
        if exists('group'):
            self.ui.edit_group_name.setText(data['group'])
        if exists('group_code'):
            self.ui.edit_group_code.setText(data['group_code'])
        if exists('faculty'):
            self.ui.edit_fac.setText(data['faculty'])
        if exists('chair'):
            self.ui.edit_chair.setText(data['chair'])
        if exists('chair_short'):
            self.ui.edit_chair_short.setText(data['chair_short'])

        if exists('study'):
            self.ui.edit_study.setText(data['study'])
        if exists('profile'):
            self.ui.edit_profile.setText(data['profile'])
        if exists('discipline_code'):
            self.ui.edit_discipline_code.setText(data['discipline_code'])
        if exists('discipline'):
            self.ui.edit_discipline.setText(data['discipline'])
        if exists('qual'):
            self.ui.edit_qual.setText(data['qual'])

    def get_info(self) -> Dict[str, str]:
        data = {
            'teacher': self.ui.edit_teacher.text().strip(),
            'teacher_duty': self.ui.edit_teacher_duty.text().strip(),
            'topic': self.ui.edit_topic.text().strip(),
            'work_type': int(self.ui.box_work_type.currentIndex() + 1),
            'year': self.ui.edit_year.text().strip(),
            'group': self.ui.edit_group_name.text().strip(),
            'group_code': self.ui.edit_group_code.text().strip(),
            'faculty': self.ui.edit_fac.text().strip(),
            'chair': self.ui.edit_chair.text().strip(),
            'chair_short': self.ui.edit_chair_short.text().strip(),
            'study': self.ui.edit_study.text().strip(),
            'profile': self.ui.edit_profile.text().strip(),
            'discipline_code': self.ui.edit_discipline_code.text().strip(),
            'discipline': self.ui.edit_discipline.text().strip(),
            'qual': self.ui.edit_qual.text().strip(),

        }
        return data
