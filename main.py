from PyQt5 import QtWidgets
from gui.gui import Program


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Program(app)
    MainWindow.show()
    sys.exit(app.exec_())

