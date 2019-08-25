# Slider.py
from PyQt5.QtWidgets import QSlider, QDialog, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import QApplication
import sys


class Slider_Dialog(QDialog):
    changedValue = pyqtSignal(int)

    def __init__(self):
        super(Slider_Dialog, self).__init__()
        self.init_ui()

    def init_ui(self):
        # Creating a lable
        sliderLabel = QLabel('Slider.', self)

        # Creating a slider and setting its maximum and minimum value
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,100)
        # self.slider.setMinimum(0)
        # self.slider.setMaximum(100)
        # self.slider.setOrientation(Qt.Horizontal)

        # Creating a horizontalBoxLayout
        hboxLayout = QHBoxLayout(self)  # Adding the widgets
        hboxLayout.addWidget(sliderLabel)
        hboxLayout.addWidget(self.slider)

        # Setting main layout
        self.setLayout(hboxLayout)
        self.setWindowTitle('Dialog with a Slider')

        # signal connecting
        self.slider.valueChanged.connect(self.on_changed_value)

        self.show()
    
    def on_changed_value(self, val):  # 슬라이더를 움직일시 발생하는 시그널을
        self.changedValue.emit(val)   # 준비된 시그널 객체로 보낸다

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sl = Slider_Dialog()
    sys.exit(app.exec_())
