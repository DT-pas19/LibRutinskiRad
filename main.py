from PyQt5 import QtWidgets
from PyQt5.QtCore import QMimeData
from gui.gui import Program

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

