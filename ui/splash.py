from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from PyQt4 import uic

import openfrontier

class SplashWidget(QWidget):
    def __init__(self, parent=None, flags=Qt.Widget):
        QWidget.__init__(self, parent, flags)
        self.bgimage = QPixmap(openfrontier.distFile('ui/splash.png'))
        
        self.buttonBox = QWidget(self)
        self.buttonBox.setLayout(QHBoxLayout())

        def createButton(text):
            newButton = QPushButton(text, self.buttonBox)
            self.buttonBox.layout().addWidget(newButton, 1)
            return newButton

        self.btnNewGame  = createButton("New Game")
        self.btnLoadGame = createButton("Load Game")

        self.buttonBox.layout().addStretch(1)

        self.btnSettings = createButton("Settings")
        self.btnQuit     = createButton("Quit")

    def resizeEvent(self, evt):
        boxHeight = 60
        self.buttonBox.setGeometry(
                0 if self.width() <= self.bgimage.width() else (self.width() - self.bgimage.width()) / 2,
                min(self.bgimage.height() - boxHeight + (self.height() - self.bgimage.height()) / 2,
                    self.height() - boxHeight),
                min(self.width(), self.bgimage.width()),
                boxHeight
                )

    def paintEvent(self, evt):
        painter = QPainter(self)
        painter.drawPixmap(
                0 if self.width() <= self.bgimage.width() else (self.width() - self.bgimage.width()) / 2,
                0 if self.height() <= self.bgimage.height() else (self.height() - self.bgimage.height()) / 2,
                self.bgimage
                )
