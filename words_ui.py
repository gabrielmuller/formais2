# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'words.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_words_of_size(object):
    def setupUi(self, words_of_size):
        words_of_size.setObjectName("words_of_size")
        words_of_size.resize(400, 300)
        self.widget = QtWidgets.QWidget(words_of_size)
        self.widget.setGeometry(QtCore.QRect(20, 20, 361, 261))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.words = QtWidgets.QPlainTextEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Noto Mono")
        self.words.setFont(font)
        self.words.setObjectName("words")
        self.verticalLayout.addWidget(self.words)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(words_of_size)
        self.buttonBox.accepted.connect(words_of_size.accept)
        self.buttonBox.rejected.connect(words_of_size.reject)
        QtCore.QMetaObject.connectSlotsByName(words_of_size)

    def retranslateUi(self, words_of_size):
        _translate = QtCore.QCoreApplication.translate
        words_of_size.setWindowTitle(_translate("words_of_size", "Enumeração de palavras"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    words_of_size = QtWidgets.QDialog()
    ui = Ui_words_of_size()
    ui.setupUi(words_of_size)
    words_of_size.show()
    sys.exit(app.exec_())

