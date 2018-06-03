from nfa import NFA
from parser import *
from regex import Regex
from window_ui import Ui_MainWindow

import copy
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QFileDialog, QListWidgetItem, QErrorMessage)

class GUI(QMainWindow, Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        #self.fa = NFA({}, "", {})
        self.fa = None
        self.rg = RegularGrammar("",{})

        self.setupUi(self)
        #self.resize(600, 400)

        # Botões
        self.regex_to_fa_button.clicked.connect(self.regex_to_fa)
        self.determinize_button.clicked.connect(self.determinize)
        self.minimize_button.clicked.connect(self.minimize)
        self.test_button.clicked.connect(self.test_word)
        self.rg_to_fa_button.clicked.connect(self.rg_to_fa)
        self.open_button.clicked.connect(self.open_fa)
        self.save_button.clicked.connect(self.save_fa)
        self.list.itemClicked.connect(self.select_fa)

        # Ações
        self.actionSalvar.triggered.connect(self.save_fa)
        self.actionAbrir.triggered.connect(self.open_fa)

        # Correspondência entre index do QListWidgetItem e autômato
        self.list_fas = []

    def select_fa(self):
        self.fa = self.list_fas[self.list.currentRow()]
        self.update_fa_table()

    def regex_to_fa(self):
        regex_str = self.regex_input.text()
        try:
            self.fa = Regex(regex_str).dfa
        except SyntaxError as e:
            self.show_error(e)
            return

        self.fa.regex_str = regex_str
        self.add_fa_to_list()

    def show_error(self, e):
        box = QErrorMessage(self) 
        box.showMessage(str(e))

    def rg_to_fa(self):
        if self.rg_text.toPlainText():
            try:
                self.rg = parse_rg(self.rg_text.toPlainText())
            except SyntaxError as e:
                self.show_error(e)
                return
                
            self.fa = NFA.from_rg(self.rg)
            self.fa.rg_str = self.rg.rg_str
            self.add_fa_to_list()

    def determinize(self):
        self.fa.determinize()
        self.add_fa_to_list()

    def minimize(self):
        self.fa.minimize()
        self.add_fa_to_list()

    def test_word(self):
        if self.fa.accepts(self.word_input.text()):
            self.statusbar.showMessage("Sentença aceita")
        else:
            self.statusbar.showMessage("Sentença rejeitada")

    def update_fa_table(self):
        # restaura regex / gramática
        if self.fa.regex_str:
            self.regex_input.setText(self.fa.regex_str)
        if self.fa.rg_str:
            self.rg_text.setPlainText(self.fa.rg_str)

        alphabet = sorted(self.fa.alphabet())
        states = []
        for state in self.fa.states():
            special = ""
            if state == '-':
                continue
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
                transition = '-'
                if state in transitions:
                    if symbol in transitions[state]:
                        transition = ", ".join(  \
                            sorted(transitions[state][symbol]))
                self.transition_table.setItem(
                    i, j, QTableWidgetItem(transition))

    def add_fa_to_list(self):
        fa = self.fa
        name = self.name_field.text()
        if name:
            fa.name = name
        self.list_fas.append(fa)
        item = QListWidgetItem(fa.name, self.list)
        self.list.setCurrentItem(item)
        self.update_fa_table()

    def save_fa(self):
        if not self.fa:
            self.show_error("Não há AF selecionado!")
            return

        path, _ = QFileDialog.getSaveFileName(self)
        if path:
            self.fa.save(path)

    def open_fa(self):
        path, _ = QFileDialog.getOpenFileName(self)
        if path:
            nfa = NFA.open(path)
            self.fa = nfa
            self.add_fa_to_list()


        
