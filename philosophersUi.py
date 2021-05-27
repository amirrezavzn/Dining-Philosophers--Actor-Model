import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtCore
import pykka
import time


class App(QWidget, pykka.ThreadingActor):

    def __init__(self, philosopher_id=1, philosopher_state="k", forks_state=0):
        super().__init__()
        self.title = "philsopher" + str(philosopher_id)
        self.philosopher_state = philosopher_state
        # self.left = 700
        # self.top = 250
        # self.width = 300
        # self.height = 580

        # centralWidget = QWidget(self)
        # self.setCentralWidget(centralWidget)
        # gridLayout = QGridLayout(self)
        # centralWidget.setLayout(gridLayout)
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        # Create widget
        label2 = QLabel(self)
        pixmap = QPixmap('drforks.png')
        label2.setPixmap(pixmap)
        title2 = QLabel("               " + self.philosopher_state, self)
        title2.setFont(QtGui.QFont('SansSerif', 13))
        # self.resize(pixmap.width(), pixmap.height())
        # self.show()
        # QtCore.QObject.connect(label2, QtCore.SIGNAL('ssss'), self.modificaton("fgvfv"))

    """ def modificaton(self, phil_state=" "):
        time.sleep(2)
        self.philosopher_state = phil_state
        title2 = QLabel("               "+self.philosopher_state)
        title2.setFont(QtGui.QFont('SansSerif', 13))"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App(1000, "eating")
    ex.setGeometry(700, 250, 300, 580)
    ex.show()
    sys.exit(app.exec_())



