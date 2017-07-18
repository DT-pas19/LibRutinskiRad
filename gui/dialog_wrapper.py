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

    def get_info(self) -> Dict:
        data = {
            'teacher': self.ui.edit_teacher.text(),
            'topic': self.ui.edit_topic.text(),
            'type' : int(self.ui.box_work_type.currentIndex() + 1),
            'year': self.ui.edit_year.text(),
            'group': self.ui.edit_group_name.text(),
            'group_code': self.ui.edit_group_code.text(),
            'faculty': self.ui.edit_fac.text()
        }
        return data
