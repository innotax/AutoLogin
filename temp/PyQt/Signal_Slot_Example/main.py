from SliderDialog.Slider import Slider_Dialog
from ProgressDialog.Progress import Progressbar_Dialog
import sys
from PyQt5.QtWidgets import QApplication

""" https://blog.naver.com/townpharm/220947288176
"""

if __name__ =='__main__':
    app = QApplication(sys.argv)
    sd = Slider_Dialog()
    pd = Progressbar_Dialog()
    pd.make_connection(sd)
    sys.exit(app.exec_())