#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
PyQt5 project 1

This program will open a file using a QFileDialog. When the user
clicks 'read', it will display the contents of the file to the screen in a QTextEdit.
The user can make edits to the file and then save it to a location by
clicking the 'save' button or in the file taskbar. The user can also simply type
in the QTextEdit box and save it, making a brand new file.

If the file has not been saved after opening, the program will double
check if the user really wants to quit, if the quit or x is clicked.

Paul Bosonetto
2/18/2017
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QTextEdit, QAction,
    QFileDialog, QApplication, QInputDialog, QPushButton, QWidget,
    QHBoxLayout, QVBoxLayout, QApplication, QMessageBox)
from PyQt5.QtGui import QIcon


#new class that is a QMainWindow
class FileEditor(QMainWindow):

    def __init__(self):
        super().__init__()

        self.savedYet = False
        self.initUI()

    def initUI(self):

        #set up text Edit
        self.textEdit = QTextEdit()
        #self.setCentralWidget(self.textEdit)
        self.statusBar()

        #Layout stuff
        openButton = QPushButton("Open")
        saveButton = QPushButton("Save")

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.textEdit)
        vbox.addWidget(openButton)
        vbox.addWidget(saveButton)

        #hbox = QHBoxLayout()
        #hbox.addStretch(1)
        #hbox.addLayout(vbox)

        window = QWidget()
        window.setLayout(vbox)

        self.setCentralWidget(window)

        #give QPushButtons functionality
        openButton.clicked.connect(self.showDialog)
        openButton.setStatusTip('Open new File')
        saveButton.clicked.connect(self.saveFile)
        saveButton.setStatusTip('Save the file')



        #Need to open a file
        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new file')
        openFile.triggered.connect(self.showDialog)

        #Need to save a file
        saveFile = QAction(QIcon('save.png'), 'Save', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save the file')
        saveFile.triggered.connect(self.saveFile)
        #fileName.write(str(textEdit.toPlainText()))

        #add open, save actions to menuBar
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(saveFile)





        #set window title and geometry, show window
        self.setGeometry(300,300,300,300)
        self.setWindowTitle('File dialog')
        self.show()



    #show the file dialog
    #display file contents to text edit
    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                self.textEdit.setText(data)

        self.savedYet = False

    def saveFile(self):
        options = QFileDialog.Options()
        #getSaveFileName returns a Tuple!!!!!!!!!
        filename = QFileDialog.getSaveFileName(self, 'Save File',"",
            "All Files (*);;Text Files (*txt)", options = options)[0]
        #alternate Version: filename, _ = QFileDialog.getSaveFileName(self, 'Save File')

        with open(filename, 'w') as file:
            file.write(str(self.textEdit.toPlainText()))

        self.textEdit.append("\n\n----------Saved!---------")

        self.savedYet = True

    def closeEvent(self, event):

        if self.savedYet == False:
            reply = QMessageBox.question(self, 'You what!???',
                "Are you sure you want to quit without saving?", QMessageBox.Yes |
                QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Fe = FileEditor()
    sys.exit(app.exec_())
