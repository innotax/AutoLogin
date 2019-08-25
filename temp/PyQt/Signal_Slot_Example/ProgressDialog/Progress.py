## Progress.py 코드 : ui 빌드업 코드
from PyQt5.QtWidgets import QDialog, QProgressBar, QLabel, QHBoxLayout, QApplication 
from PyQt5.QtCore import pyqtSlot
import sys

class Progressbar_Dialog(QDialog):
    def __init__(self):
        super(Progressbar_Dialog, self).__init__()
        self.init_ui()

    def init_ui(self):
        # Creating a label
        progressLabel = QLabel('ProgressBar.',self)

        # Creating a progress bar and setting the value limits
        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)

        # Creating a Horizontal Layout to add all the widgets
        hboxLayout = QHBoxLayout(self)
        # Adding the widgets
        hboxLayout.addWidget(progressLabel)
        hboxLayout.addWidget(self.progressBar)

        # Setting the hBoxLayout as the main layout
        self.setLayout(hboxLayout)
        self.setWindowTitle('Dialog with Progressbar')

        self.show()

    def make_connection(self, slider_object):
        slider_object.changedValue.connect(self.get_slider_value) # 1. 슬라이더에서 발생한 시그널을 연결하도록 도와주는 합수 생성

    @pyqtSlot(int)  # int type pyqtSlot 이 있을때만 실행된다
    def get_slider_value(self, val):                              # 2. 연결함수를 통해 전달된 시그널에 반응하는 함수를 생성
        self.progressBar.setValue(val)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pb = Progressbar_Dialog()
    sys.exit(app.exec_())
