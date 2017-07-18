import os

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QHeaderView

from document_processor import read_data
from gui.common_options_dialog import Ui_Dialog
from gui.dialog_wrapper import DialogWrapper
from gui.paperlibroutine import Ui_MainWindow
from table_models import FileCheckModel


class Program(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file_selection_model = FileCheckModel()
        self.setup_widgets()

    def setup_widgets(self):
        self.ui.edit_path.editingFinished.connect(self.update_filelist)
        self.ui.btn_file_dialog.clicked.connect(self.call_file_dialog)

        self.ui.table_files_view.setModel(self.file_selection_model)
        self.ui.table_files_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        # @see stackoverflow.com/questions/3433664/how-to-make-sure-columns-in-qtableview-are-resized-to-the-maximum

        tab_switch = lambda x: self.ui.tab_widget.setCurrentIndex(x)
        # на уровень выше, нужно при работе с файлом перелистывать на начало
        # self.ui.btn_start_reading.clicked.connect(lambda checked, i=1: tab_switch(i))
        self.ui.btn_start_reading.clicked.connect(self.start_reading)
        self.ui.btn_back_choosing.clicked.connect(lambda checked, i=0: tab_switch(i))

        self.ui.btn_change.clicked.connect(self.open_dialog)

    def start_reading(self, checked):
        necessary_data = self.file_selection_model.get_data()
        self.ui.tab_widget.setCurrentIndex(1)  # при переключении вкладки флажки в таблице сбрасываются и везде False
        self.file_selection_model.restore_data(necessary_data)
        print('Начинаем чтение')
        files = [file for file, is_checked in necessary_data if is_checked]
        folder = self.ui.edit_path.text()
        result = read_data(folder=folder, files=files)

    def open_dialog(self):
        change_dialog = DialogWrapper(self)
        change_dialog.show()

        def accept_changes():
            result = change_dialog.get_info()
            print(result)
        change_dialog.ui.btn_apply.accepted.connect(accept_changes)

    def update_filelist(self):
        path = self.ui.edit_path.text()
        flag = os.path.exists(path) and os.path.isdir(path)

        print('Путь: {} ({})'.format(path, '+' if flag else '-'))
        if not flag:
            return

        contents = [item for item in os.listdir(path) if os.path.isfile(os.path.join(path, item))]
        self.file_selection_model.clear()
        self.file_selection_model.append(contents)
        # checkbox в таблице + обновление модели

    def call_file_dialog(self):
        """
        Вызов диалога выбора папки
        :return:
        """
        options = QFileDialog.Options() | QFileDialog.DontUseNativeDialog | \
                  QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks

        dir_name = QFileDialog.getExistingDirectory(self, "Укажите папку с работами", os.getcwd(), options=options)
        if dir_name:
            print("Выбрана папка {}".format(dir_name))
            self.ui.edit_path.setText(dir_name)
            self.update_filelist()

    def create_plot(self):
        self.model = QtGui.QStandardItemModel(self)

        for rowName in range(3) * 5:
            self.model.invisibleRootItem().appendRow(
                [QtGui.QStandardItem("row {0} col {1}".format(rowName, column))
                 for column in range(3)
                 ]
            )

        self.proxy = QtGui.QSortFilterProxyModel(self)
        self.proxy.setSourceModel(self.model)

        self.view.setModel(self.proxy)

# таблица на стр 2
# имя студента | файл | тема работы | факультет
# тема | вид работы | год | специальность | факультет

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Program()
    MainWindow.show()
    sys.exit(app.exec_())
