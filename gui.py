from nfa import NFA
from parser import *
from regex import Regex
from window_ui import Ui_MainWindow

import copy
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QFileDialog)

class GUI(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.fa = NFA({}, "", {})
        self.rg = RegularGrammar("",{})

        self.setupUi(self)
        #self.resize(600, 400)

        # Botões
        self.regex_to_fa_button.clicked.connect(self.regex_to_fa)
        self.determinize_button.clicked.connect(self.determinize)
        self.minimize_button.clicked.connect(self.minimize)
        self.test_button.clicked.connect(self.test_word)
        self.rg_to_fa_button.clicked.connect(self.rg_to_fa)

        # Ações
        self.actionSalvar.triggered.connect(self.save_fa)
        self.actionAbrir.triggered.connect(self.open_fa)

    def regex_to_fa(self):
        regex_str = self.regex_input.text()
        self.fa = Regex(regex_str).dfa
        self.update_fa_table()

    def rg_to_fa(self):
        if (self.rg_text.toPlainText()):
            self.rg = parse_rg(self.rg_text.toPlainText())
            self.fa = NFA.from_rg(self.rg)
            self.update_fa_table()

    def determinize(self):
        self.fa.determinize()
        self.update_fa_table()

    def minimize(self):
        self.fa.minimize()
        self.update_fa_table()

    def test_word(self):
        if self.fa.accepts(self.word_input.text()):
            self.statusbar.showMessage("Sentença aceita")
        else:
            self.statusbar.showMessage("Sentença rejeitada")

    def update_fa_table(self):
        alphabet = self.fa.alphabet()
        states = []
        for state in self.fa.states():
            special = ""
            if state in self.fa.accepting:
                special += "*"
            if state in self.fa.initial:
                special += "->"
            states.append(special + state)

        self.transition_table.setRowCount(len(states))
        self.transition_table.setColumnCount(len(alphabet))
        self.transition_table.setVerticalHeaderLabels(states)
        self.transition_table.setHorizontalHeaderLabels(alphabet)

        transitions = self.fa.transitions
        for i, state in enumerate(self.fa.states()):
            for j, symbol in enumerate(alphabet):
                if state in transitions:
                    if symbol in transitions[state]:
                        transition = ",".join(  \
                            sorted(transitions[state][symbol]))
                self.transition_table.setItem(
                    i, j, QTableWidgetItem(transition))

    def save_fa(self):
        path, _ = QFileDialog.getSaveFileName(self)
        if path:
            self.fa.save(path)

    def open_fa(self):
        path, _ = QFileDialog.getOpenFileName(self)
        if path:
            nfa = NFA.open(path)
            self.fa = nfa
            self.update_fa_table()


        
