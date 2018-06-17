from cfg import Grammar
from reader import *
from window_ui import Ui_MainWindow

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QFileDialog, QListWidgetItem, 
    QErrorMessage, QDialog)

class GUI(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        #self.cfg
        self.cfg = None

        self.setupUi(self)
        #self.resize(600, 400)

        # Botões
        self.saveGrammarButton.clicked.connect(self.create_grammar)
        self.grammarList.itemClicked.connect(self.select_grammar)

        # Correspondência entre index do QListWidgetItem e gramática
        self.cfg_list = []

    def select_grammar(self):
        self.cfg = self.cfg_list[self.grammarList.currentRow()]
        self.update_cfg_text()

    def create_grammar(self):
        if self.grammarText.toPlainText():
            try:
                self.cfg = Grammar(self.grammarText.toPlainText())
            except SyntaxError as e:
                self.show_error(e)
                return
            self.add_grammar_to_list()
        else:
            self.show_error("Defina uma gramática!")
            return

    def add_grammar_to_list(self):
        cfg = self.cfg
        name = self.nameField.text()
        if name:
            cfg.name = name
        self.cfg_list.append(cfg)
        item = QListWidgetItem(cfg.name, self.grammarList)
        self.grammarList.setCurrentItem(item)


    def update_cfg_text(self):
        self.grammarText.setPlainText(self.cfg.to_string())

    def show_error(self, e):
        box = QErrorMessage(self) 
        box.showMessage(str(e))