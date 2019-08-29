from PyQt5 import QtCore, QtGui, QtWidgets
from selenium import webdriver
import time
import threading
from bs4 import BeautifulSoup as soup
import requests

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(388, 179)
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 100, 271, 21))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic")
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color: transparent;\n"
"color: rgb(255, 255, 255);")
        self.lineEdit_2.setObjectName("lineEdit_2")

class Dialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

       # self.pushButton.pressed.connect(self.textEdit.clear)
       # self.pushButton.pressed.connect(self.sejd)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.keyworddict = {}
        self.count = {}
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(803, 538)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        MainWindow.setMaximumSize(QtCore.QSize(10000, 10000))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(180, 210, 75, 23))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic")
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralWidget)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.pushButton.pressed.connect(self.on_Button_clicked)

    def on_Button_clicked(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_Dialog()
        dialog.ui.setupUi(dialog)

        # connect signal to slot
        dialog.ui.lineEdit_2.textChanged.connect(self.dialogTextChanged)
        dialog.setWindowTitle("Login")
        # dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            text = dialog.ui.lineEdit_2.text()

        # print(dialog.ui.lineEdit_2.text())
        dialog.deleteLater()
    
    def dialogTextChanged(self, text):
        print(text)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle("ui")
    w.show()
    sys.exit(app.exec_())