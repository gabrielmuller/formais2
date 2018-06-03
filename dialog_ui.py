# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(356, 208)
        self.op_buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.op_buttonBox.setGeometry(QtCore.QRect(10, 170, 341, 32))
        self.op_buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.op_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.op_buttonBox.setObjectName("op_buttonBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 341, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fa_1_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.fa_1_label.setObjectName("fa_1_label")
        self.horizontalLayout.addWidget(self.fa_1_label, 0, QtCore.Qt.AlignHCenter)
        self.fa_1_combo = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.fa_1_combo.setObjectName("fa_1_combo")
        self.horizontalLayout.addWidget(self.fa_1_combo)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 60, 341, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.fa_2_label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.fa_2_label.setObjectName("fa_2_label")
        self.horizontalLayout_2.addWidget(self.fa_2_label, 0, QtCore.Qt.AlignHCenter)
        self.fa_2_combo = QtWidgets.QComboBox(self.horizontalLayoutWidget_2)
        self.fa_2_combo.setObjectName("fa_2_combo")
        self.horizontalLayout_2.addWidget(self.fa_2_combo)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 110, 341, 41))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.intersection_radio = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        self.intersection_radio.setObjectName("intersection_radio")
        self.horizontalLayout_3.addWidget(self.intersection_radio)
        self.difference_radio = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        self.difference_radio.setEnabled(True)
        self.difference_radio.setObjectName("difference_radio")
        self.horizontalLayout_3.addWidget(self.difference_radio)
        self.reverse_radio = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        self.reverse_radio.setObjectName("reverse_radio")
        self.horizontalLayout_3.addWidget(self.reverse_radio)

        self.retranslateUi(Dialog)
        self.op_buttonBox.accepted.connect(Dialog.accept)
        self.op_buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Operações"))
        self.fa_1_label.setText(_translate("Dialog", "AF 1"))
        self.fa_2_label.setText(_translate("Dialog", "AF 2"))
        self.intersection_radio.setText(_translate("Dialog", "Intersecção"))
        self.difference_radio.setText(_translate("Dialog", "Diferença"))
        self.reverse_radio.setText(_translate("Dialog", "Reverso"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

