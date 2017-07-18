# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'common_options_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.dev1706151807
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(408, 333)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.btn_apply = QtWidgets.QDialogButtonBox(Dialog)
        self.btn_apply.setGeometry(QtCore.QRect(130, 290, 271, 32))
        self.btn_apply.setOrientation(QtCore.Qt.Horizontal)
        self.btn_apply.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.btn_apply.setObjectName("btn_apply")
        self.formLayoutWidget = QtWidgets.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 306))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.lbl_teacher = QtWidgets.QLabel(self.formLayoutWidget)
        self.lbl_teacher.setObjectName("lbl_teacher")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbl_teacher)
        self.edit_teacher = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.edit_teacher.setObjectName("edit_teacher")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.edit_teacher)
        self.lbl_topic = QtWidgets.QLabel(self.formLayoutWidget)
        self.lbl_topic.setObjectName("lbl_topic")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_topic)
        self.edit_topic = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.edit_topic.setObjectName("edit_topic")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.edit_topic)
        self.lbl_work_type = QtWidgets.QLabel(self.formLayoutWidget)
        self.lbl_work_type.setObjectName("lbl_work_type")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lbl_work_type)
        self.box_work_type = QtWidgets.QComboBox(self.formLayoutWidget)
        self.box_work_type.setMinimumSize(QtCore.QSize(200, 0))
        self.box_work_type.setObjectName("box_work_type")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.box_work_type)
        self.lbl_year = QtWidgets.QLabel(self.formLayoutWidget)
        self.lbl_year.setObjectName("lbl_year")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.lbl_year)
        self.edit_year = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.edit_year.setMaximumSize(QtCore.QSize(80, 16777215))
        self.edit_year.setObjectName("edit_year")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.edit_year)
        self.lbl_group_name = QtWidgets.QLabel(self.formLayoutWidget)
        self.lbl_group_name.setObjectName("lbl_group_name")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.lbl_group_name)
        self.edit_group_name = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.edit_group_name.setMaximumSize(QtCore.QSize(200, 16777215))
        self.edit_group_name.setObjectName("edit_group_name")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.edit_group_name)
        self.lbl_fac = QtWidgets.QLabel(self.formLayoutWidget)
        self.lbl_fac.setObjectName("lbl_fac")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.lbl_fac)
        self.edit_fac = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.edit_fac.setMaximumSize(QtCore.QSize(500, 16777215))
        self.edit_fac.setObjectName("edit_fac")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.edit_fac)
        self.lbl_group_code = QtWidgets.QLabel(self.formLayoutWidget)
        self.lbl_group_code.setObjectName("lbl_group_code")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.lbl_group_code)
        self.edit_group_code = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.edit_group_code.setMaximumSize(QtCore.QSize(100, 16777215))
        self.edit_group_code.setObjectName("edit_group_code")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.edit_group_code)

        self.retranslateUi(Dialog)
        self.btn_apply.accepted.connect(Dialog.accept)
        self.btn_apply.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Изменение общих параметров"))
        self.lbl_teacher.setText(_translate("Dialog", "Руководитель"))
        self.lbl_topic.setText(_translate("Dialog", "Тема работы"))
        self.lbl_work_type.setText(_translate("Dialog", "Вид"))
        self.lbl_year.setText(_translate("Dialog", "Год"))
        self.lbl_group_name.setText(_translate("Dialog", "Специальность"))
        self.lbl_fac.setText(_translate("Dialog", "<html><head/><body><p>Фак/инст.</p></body></html>"))
        self.lbl_group_code.setText(_translate("Dialog", "Код"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

