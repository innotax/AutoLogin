
'''
import sys
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
inputbox = QInputDialog()
inputbox.show()
# txt, ok = inputbox.getText('QLineEdit.Normal')
# if ok:
#     print(txt)
sys.exit(app.exec_())
'''
from abaqus import getInput
from math import sqrt
number = float(getInput('Enter a number:'))
print (sqrt(number))

