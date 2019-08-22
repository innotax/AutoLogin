import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class MsgBoxTF(QMessageBox):

    def __init__(self, title="QMessageBox", msg=None):
        super().__init__()
        self.title = title
        self.msg = msg

        rect = QDesktopWidget().availableGeometry()   # 작업표시줄 제외한 화면크기 반환
        max_x = rect.width()
        max_y = rect.height()

        self.width = 320
        self.height = 200
        # self.left = max_x - self.width 
        # self.top = max_y - self.height
        # 윈도우 중간
        self.left = max_x / 2
        self.top = max_y /2 
        
        self.initUI()
        
    def initUI(self):
        # self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        buttonReply = QMessageBox.question(self, self.title, self.msg, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            return True
            # print('Yes clicked.')
        else:
            return False
            # print('No clicked.')

        # self.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MsgBoxTF()
    sys.exit(app.exec_())  