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
        self.glcPropriaButton.clicked.connect(self.proper)

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

    def proper(self):
        # Transforma em própria e mostra intermediárias e conjuntos
        if self.cfg:
            # G sem símbolos inférteis
            self.resultText_1.setPlainText("Nf = " + str(self.cfg.fertile()))
            g = self.cfg.remove_infertile()
            self.resultText_1.appendPlainText("\n    Sem símbolos inférteis:")
            self.resultText_1.appendPlainText(str(g))

            # G sem símbolos inalcançáveis
            self.resultText_1.appendPlainText("\nVi = " + str(g.reachable()))
            g = g.rm_unreachable()
            self.resultText_1.appendPlainText("\n   Sem símbolos inalcançáveis:")
            self.resultText_1.appendPlainText(str(g))

            # G ε-livre
            self.resultText_1.appendPlainText("\nNe = " + str(g.nullable()))
            g = g.epsilon_free()
            self.resultText_1.appendPlainText("\n    ε-livre:")
            self.resultText_1.appendPlainText(str(g))

            # G sem produções simples (sem ciclos?)
            self.resultText_1.appendPlainText("")
            g = g.rm_simple()
            self.resultText_1.appendPlainText("\n    Sem produções simples:\n   G Própria:")
            self.resultText_1.appendPlainText(str(g)) 
     
            g.name = self.cfg.name + " Própria"

            self.add_result_grammar_to_list(g)

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

    def add_result_grammar_to_list(self, result_cfg):
        self.cfg_list.append(result_cfg)
        item = QListWidgetItem(result_cfg.name, self.grammarList)

    def update_cfg_text(self):
        self.grammarText.setPlainText(str(self.cfg))

    def update_info_label(self):
        empty = "vazia" if self.cfg.isEmpty() else "não-vazia"
        finite = "finita" if self.cfg.isFinite() else "infinita"

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