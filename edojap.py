#!/usr/bin/env python3
from numbers_parser import Document
from PyQt5 import QtWidgets
from random import randint
import sys


class MainWindow(QtWidgets.QMainWindow):


    doc = None
    tabella = []
    main_layout = None
    carica_file = None
    carica_file_label = None
    carica_file_btn = None
    scegli_tabella = None
    scegli_tabella_dropdown = None
    carica_tabella_btn = None
    quiz = None
    quiz_domanda_label = None
    quiz_risposta_btn = None
    quiz_risposta_label = None
    quiz_prossima_btn = None


    def __init__(self):
        super().__init__()

        self.setWindowTitle("EdoJap")

        self.main_layout = QtWidgets.QVBoxLayout()
        self.carica_file = QtWidgets.QHBoxLayout()
        self.carica_file_label = QtWidgets.QLabel("Apri file:")
        self.carica_file_btn = QtWidgets.QPushButton("Apri...")
        self.scegli_tabella = QtWidgets.QHBoxLayout()
        self.scegli_tabella_dropdown = QtWidgets.QComboBox()
        self.carica_tabella_btn = QtWidgets.QPushButton("Apri tabella")
        self.quiz = QtWidgets.QHBoxLayout()
        self.quiz_domanda_label = QtWidgets.QLabel("Indovina:")
        self.quiz_risposta_btn = QtWidgets.QPushButton("Risposta?")
        self.quiz_risposta_label = QtWidgets.QLabel("Risposta:")
        self.quiz_prossima_btn = QtWidgets.QPushButton("Prossima!")

        self.carica_file_btn.pressed.connect(self.carica_file_click)

        self.carica_file.addWidget(self.carica_file_label)
        self.carica_file.addWidget(self.carica_file_btn)
        self.main_layout.addLayout(self.carica_file)
        self.scegli_tabella_dropdown.currentIndexChanged.connect(self.scegli_tabella_changed)
        self.scegli_tabella.addWidget(self.scegli_tabella_dropdown)
        self.carica_tabella_btn.pressed.connect(self.carica_tabella_click)
        self.carica_tabella_btn.setEnabled(False)
        self.scegli_tabella.addWidget(self.carica_tabella_btn)
        self.main_layout.addLayout(self.scegli_tabella)
        self.quiz.addWidget(self.quiz_domanda_label)
        self.quiz.addWidget(self.quiz_risposta_btn)
        self.quiz_risposta_btn.pressed.connect(self.risposta_click)
        self.quiz_risposta_btn.setEnabled(False)
        self.quiz.addWidget(self.quiz_risposta_label)
        self.quiz_prossima_btn.pressed.connect(self.prossima_click)
        self.quiz_prossima_btn.setEnabled(False)
        self.quiz.addWidget(self.quiz_prossima_btn)
        self.main_layout.addLayout(self.quiz)

        w = QtWidgets.QWidget()
        w.setLayout(self.main_layout)
        self.setCentralWidget(w)
        self.show()


    def carica_file_click(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home/wasp/personal/edo/', 'Numbers files (*.numbers)')
        self.doc = Document(fname[0])
        self.scegli_tabella_dropdown.clear()
        for table in self.doc.sheets[0].tables:
            self.scegli_tabella_dropdown.addItem(table.name)


    def scegli_tabella_changed(self, i):
        self.carica_tabella_btn.setEnabled(True)
    

    def set_domanda_random(self):
        scelta_random = self.tabella.pop(randint(0, len(self.tabella)-1))
        self.quiz_domanda_label.setText(scelta_random[0])
        self.quiz_risposta_label.setVisible(False)
        self.quiz_risposta_label.setText(scelta_random[1])
        self.quiz_risposta_btn.setEnabled(True)
        self.quiz_prossima_btn.setEnabled(False)


    def carica_tabella_click(self):
        self.tabella = [[row[0].value, row[1].value] for row in self.doc.sheets[0].tables[self.scegli_tabella_dropdown.currentText()].rows()]
        self.tabella.pop(0)
        self.set_domanda_random()


    def risposta_click(self):
        self.quiz_risposta_label.setVisible(True)
        self.quiz_risposta_btn.setEnabled(False)
        self.quiz_prossima_btn.setEnabled(True)

    
    def prossima_click(self):
        if len(self.tabella) > 0:
            self.set_domanda_random()    
        else:
            self.quiz_prossima_btn.setEnabled(False)
            QtWidgets.QMessageBox.warning(self, "Attenzione", "Tabella finita! Clicca di nuovo carica tabella o cambiala.")
        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec()
