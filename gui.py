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
        self.firstButton.clicked.connect(self.first)
        self.firstNtButton.clicked.connect(self.first_nt)
        self.followButton.clicked.connect(self.follow)

        # Lista
        self.grammarList.itemClicked.connect(self.select_grammar)

        # Correspondência entre index do QListWidgetItem e gramática
        self.cfg_list = []

    """
        Callbacks
    """
    def select_grammar(self):
        self.cfg = self.cfg_list[self.grammarList.currentRow()]
        self.update_cfg_text()
        self.update_info_label()

    def create_grammar(self):
        if self.grammarText.toPlainText():
            try:
                self.cfg = Grammar(self.grammarText.toPlainText())
            except SyntaxError as e:
                self.show_error(e)
                return
            self.add_grammar_to_list()
            self.update_info_label()
        else:
            self.show_error("Defina uma gramática!")
            return

    def first(self):
        if self.cfg:
            self.resultText_1.setPlainText(
                self.first_string(self.cfg.first(), "FIRST"))

    def first_nt(self):
        if self.cfg:
            self.resultText_1.setPlainText(
                self.first_string(self.cfg.first_nt(), "FIRST-NT"))

    def follow(self):
        if self.cfg:
            self.resultText_1.setPlainText(
                self.first_string(self.cfg.follow(), "FOLLOW"))

    """
        Auxiliares
    """
    def add_grammar_to_list(self):
        cfg = self.cfg
        name = self.nameField.text()
        if name:
            cfg.name = name
        self.cfg_list.append(cfg)
        item = QListWidgetItem(cfg.name, self.grammarList)
        self.grammarList.setCurrentItem(item)

    def update_cfg_text(self):
        self.grammarText.setPlainText(str(self.cfg))

    def update_info_label(self):
        # TODO:
        #empty = self.cfg.isEmpty() ? "vazia" : "não-vazia"
        #finite = self.cfg.isFinite() ? "finita" : "infinita"

        empty = "não-vazia"
        finite = "finita"

        info = "Gramática é: " + empty + " e " + finite + "."
        self.infoLabel.setText(info)

    def show_error(self, e):
        box = QErrorMessage(self) 
        box.showMessage(str(e))

    # Recebe dicionario e retorna string
    def first_string(self, first_dict, op):
        line = ""
        string = ""
        for vn in first_dict.keys():
            line = op + "(" + vn + ") = "
            for vn in first_dict[vn]:
                line = line + vn + ", "
            if line[len(line)-2] != "=":
                line = line[:len(line)-2]
            line += '\n'
            string += line
        return string