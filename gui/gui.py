from model.reader import *
from model.cfg import Grammar
from gui.window_ui import Ui_MainWindow

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QFileDialog, QListWidgetItem, 
    QErrorMessage, QDialog, QInputDialog, QMessageBox)

# Mensagem de erro
UNDEFINED_ERR_MSG =  "Defina uma gramática! (e salve-a!)"

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
        self.factorButton.clicked.connect(self.factored)
        self.firstNtButton.clicked.connect(self.first_nt)
        self.followButton.clicked.connect(self.follow)
        self.properButton.clicked.connect(self.proper)
        self.firstButton.clicked.connect(self.first)
        
        # Lista
        self.grammarList.currentItemChanged.connect(self.select_grammar)

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
            self.show_error(UNDEFINED_ERR_MSG)
            return

    def first(self):
        if self.cfg:
            self.resultText_1.setPlainText(
                self.first_string(self.cfg.first(), "FIRST"))
        else:
            self.show_error(UNDEFINED_ERR_MSG)
            return

    def first_nt(self):
        if self.cfg:
            self.resultText_1.setPlainText(
                self.first_string(self.cfg.first_nt(), "FIRST-NT"))
        else:
            self.show_error(UNDEFINED_ERR_MSG)
            return

    def follow(self):
        if self.cfg:
            self.resultText_1.setPlainText(
                self.first_string(self.cfg.follow(), "FOLLOW"))
        else:
            self.show_error()
            return

    def proper(self):
        # Transforma em própria e mostra intermediárias e conjuntos
        if self.cfg:
            if self.cfg.is_proper():
                self.show_error("Gramática já é Própria.")
                return
            # G sem símbolos inférteis
            sset = str(self.cfg.fertile() or "Ø")
            g = self.cfg.remove_infertile()
            resultText = "Nf = " + sset + "\n\n    G' sem símbolos inférteis:\n" + str(g)
            self.resultText_1.setPlainText(resultText)

            # G sem símbolos inalcançáveis
            sset = str(g.reachable() or "Ø")
            g = g.rm_unreachable()
            resultText = "\nVi = " + sset + "\n\n    G'' sem símbolos inalcançáveis:\n" + str(g)
            self.resultText_1.appendPlainText(resultText)

            # G ε-livre
            sset = str(g.nullable() or "Ø")
            g = g.epsilon_free()
            resultText = "\nNe = " + sset + "\n\n    G''' ε-livre:\n" + str(g)
            self.resultText_1.appendPlainText(resultText)

            # G sem produções simples (sem ciclos?)

            na = self.first_string(g._simple_star(), "N")
            g = g.rm_simple()
            resultText = "\n" + str(na) + "\n     G'''' Sem produções simples:\n" + str(g)
            self.resultText_1.appendPlainText(resultText)

            g.name = self.cfg.name + " Própria"
            self.add_result_grammar_to_list(g)
        else:
            self.show_error(UNDEFINED_ERR_MSG)
            return

    def factored(self):
        if self.cfg:
            # Caso G não fatorada
            if not self.cfg.is_factored():
                
                # Input número de passos de fatoração
                dialog = QInputDialog()
                dialog.setInputMode(QInputDialog.IntInput)
                dialog.setIntRange (1, 10)
                steps, ok = dialog.getInt(self, 'Passos de fatoração', \
                    'Defina o número de passos:')
                if not ok or not steps:
                    return

                # Fatoração
                try:
                    g = self.cfg.factor_in_steps(steps)
                    self.resultText_1.setPlainText(str(g))
                    stepText = " passos" if steps>1 else " passo"
                    g.name = self.cfg.name + " Fatorada "
                    self.add_result_grammar_to_list(g)
                except Exception as e:
                    self.resultText_1.setPlainText(str(e))

            else:
                self.show_error("Gramática já está fatorada.")
            return

        else:
            self.show_error(UNDEFINED_ERR_MSG)
            return

    def leftRecursion(self):
        if self.cfg:
            direct_rec = self.cfg.has_direct_left_recursion()
            indirect_rec = self.cfg.has_indirect_left_recursion()

            try:
                g = self.cfg.remove_left_recursion()
            except ValueError:
                self.show_error("Gramática deve ser própria!")
                return

            # Interface
            self.resultText_1.setPlainText("Não-terminais com rec. a esquerda direta: " + \
                str(direct_rec or 'Ø') + '\n')
            self.resultText_1.appendPlainText("Não-terminais com rec. a esquerda indireta: " + \
                str(indirect_rec or 'Ø') + '\n')
            self.resultText_1.appendPlainText(str(g))
            g.name = self.cfg.name + " sem Rec. a Esquerda"
            self.add_result_grammar_to_list(g)
        else:
            self.show_error(UNDEFINED_ERR_MSG)
            return

    """
        Auxiliares
    """
    def add_grammar_to_list(self):
        cfg = self.cfg
        name = self.nameField.text()
        if name:
            cfg.name = name
        self.add_result_grammar_to_list(cfg)

    def add_result_grammar_to_list(self, result_cfg):
        self.cfg_list.append(result_cfg)
        item = QListWidgetItem(result_cfg.name, self.grammarList)
        self.grammarList.setCurrentItem(item)

    def update_cfg_text(self):
        self.grammarText.setPlainText(str(self.cfg))

    def update_info_label(self):
        empty = "vazia" if self.cfg.isEmpty() else "não-vazia"
        finite = "finita" if self.cfg.isFinite() else "infinita"
        factored = "Fatorada." if self.cfg.is_factored() else "Não-fatorada."

        info = "Gramática é: " + empty + " e " + finite + ". " + factored 
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
