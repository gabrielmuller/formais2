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

        # PlainTextEdit
        self.resultText_1.setReadOnly(True)

        # Botões
        self.leftRecursionButton.clicked.connect(self.leftRecursion)
        self.saveGrammarButton.clicked.connect(self.create_grammar)
        self.fatoradaButton.clicked.connect(self.factored)
        self.firstNtButton.clicked.connect(self.first_nt)
        self.followButton.clicked.connect(self.follow)
        self.properButton.clicked.connect(self.proper)
        self.firstButton.clicked.connect(self.first)
        
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
            self.show_error("Defina uma gramática! (e salve-a!)")
            return

    def first(self):
        if self.cfg:
            self.resultText_1.setPlainText(
                self.first_string(self.cfg.first(), "FIRST"))
        else:
            self.show_error("Defina uma gramática! (e salve-a!)")
            return

    def first_nt(self):
        if self.cfg:
            self.resultText_1.setPlainText(
                self.first_string(self.cfg.first_nt(), "FIRST-NT"))
        else:
            self.show_error("Defina uma gramática! (e salve-a!)")
            return

    def follow(self):
        if self.cfg:
            self.resultText_1.setPlainText(
                self.first_string(self.cfg.follow(), "FOLLOW"))
        else:
            self.show_error("Defina uma gramática! (e salve-a!)")
            return

    def proper(self):
        # Transforma em própria e mostra intermediárias e conjuntos
        if self.cfg:
            # G sem símbolos inférteis
            sset = str(self.cfg.fertile()) if self.cfg.fertile() else "Ø"
            g = self.cfg.remove_infertile()
            resultText = "Nf = " + sset + "\n\n    Sem símbolos inférteis:" + '\n' + str(g)
            self.resultText_1.setPlainText(resultText)

            # G sem símbolos inalcançáveis
            sset = str(self.cfg.fertile()) if g.reachable() else "Ø"
            g = g.rm_unreachable()
            resultText = "\nVi = " + sset + "\n\n    Sem símbolos inalcançáveis:" + '\n' + str(g)
            self.resultText_1.appendPlainText(resultText)

            # G ε-livre
            sset = str(self.cfg.fertile()) if g.nullable() else "Ø"
            g = g.epsilon_free()
            resultText = "\nNe = " + sset + "\n\n    ε-livre:" + '\n' + str(g)
            self.resultText_1.appendPlainText(resultText)

            # G sem produções simples (sem ciclos?)
            na = {c for c in g._simple_star().keys()}
            g = g.rm_simple()
            resultText = "\nNa = " + str(na) + "\n\n     Sem produções simples:\n   G Própria:" + '\n' + str(g)
            self.resultText_1.appendPlainText(resultText)

            g.name = self.cfg.name + " Própria"

            self.add_result_grammar_to_list(g)
        else:
            self.show_error("Defina uma gramática! (e salve-a!)")
            return

    def leftRecursion(self):
        if self.cfg:
            self.resultText_1.setPlainText("placeholder")
        else:
            self.show_error("Defina uma gramática! (e salve-a!)")
            return

    def factored(self):
        if self.cfg:
            result = "Fatorada." if self.cfg.is_factored() else "Não-fatorada."
            self.resultText_1.setPlainText(result)
        else:
            self.show_error("Defina uma gramática! (e salve-a!)")
            return

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