# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_gr.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(504, 334)
        self.op_rg_buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.op_rg_buttonBox.setGeometry(QtCore.QRect(310, 300, 191, 32))
        self.op_rg_buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.op_rg_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.op_rg_buttonBox.setObjectName("op_rg_buttonBox")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 290, 291, 41))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.unionrg_radio = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        self.unionrg_radio.setObjectName("unionrg_radio")
        self.horizontalLayout_3.addWidget(self.unionrg_radio)
        self.concatenation_radio = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        self.concatenation_radio.setObjectName("concatenation_radio")
        self.horizontalLayout_3.addWidget(self.concatenation_radio)
        self.kleene_radio = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        self.kleene_radio.setEnabled(True)
        self.kleene_radio.setObjectName("kleene_radio")
        self.horizontalLayout_3.addWidget(self.kleene_radio)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 241, 271))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rg_1_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.rg_1_label.setObjectName("rg_1_label")
        self.horizontalLayout.addWidget(self.rg_1_label)
        self.import_gr_1_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.import_gr_1_button.setObjectName("import_gr_1_button")
        self.horizontalLayout.addWidget(self.import_gr_1_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.rg_1_input = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget)
        self.rg_1_input.setObjectName("rg_1_input")
        self.verticalLayout.addWidget(self.rg_1_input)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(260, 10, 241, 271))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rg_2_label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.rg_2_label.setObjectName("rg_2_label")
        self.horizontalLayout_2.addWidget(self.rg_2_label, 0, QtCore.Qt.AlignHCenter)
        self.import_gr_2_button = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.import_gr_2_button.setObjectName("import_gr_2_button")
        self.horizontalLayout_2.addWidget(self.import_gr_2_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.rg_2_input = QtWidgets.QPlainTextEdit(self.verticalLayoutWidget_2)
        self.rg_2_input.setObjectName("rg_2_input")
        self.verticalLayout_2.addWidget(self.rg_2_input)

        self.retranslateUi(Dialog)
        self.op_rg_buttonBox.accepted.connect(Dialog.accept)
        self.op_rg_buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Operações"))
        self.unionrg_radio.setText(_translate("Dialog", "União"))
        self.concatenation_radio.setText(_translate("Dialog", "Concatenação"))
        self.kleene_radio.setText(_translate("Dialog", "Fechamento"))
        self.rg_1_label.setText(_translate("Dialog", "GR 1"))
        self.import_gr_1_button.setText(_translate("Dialog", "Importar"))
        self.rg_2_label.setText(_translate("Dialog", "GR 2"))
        self.import_gr_2_button.setText(_translate("Dialog", "Importar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

