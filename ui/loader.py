from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import openfrontier

from .prefs  import PrefsDialog

class LoaderWindow(QWidget):
    '''
    Initial splash/menu screen
    '''
    def __init__(self, parent=None, flags=Qt.Widget):
        QWidget.__init__(self, parent, flags)
        self.bgimage = QPixmap(openfrontier.distFile('ui/splash.png'))

        self.buttonBox = QWidget(self)
        self.buttonBox.setLayout(QHBoxLayout())

        def createButton(text, **kwargs):
            newButton = QPushButton(text, self.buttonBox, **kwargs)
            self.buttonBox.layout().addWidget(newButton, 1)
            return newButton

        self.btnNewGame  = createButton("New Game", clicked=self.newGame)
        self.btnLoadGame = createButton("Load Game", clicked=self.loadGame)

        self.buttonBox.layout().addStretch(1)

        self.btnSettings = createButton("Settings", clicked=self.showSettings)
        self.btnQuit     = createButton("Quit", clicked=qApp.quit)

    @pyqtSlot()
    def newGame(self):
        pass

    @pyqtSlot()
    def loadGame(self):
        pass

    @pyqtSlot()
    def showSettings(self):
        dlg = PrefsDialog(self)
        dlg.setWindowModality(Qt.WindowModal)
        dlg.show()

    def sizeHint(self):
        return self.bgimage.size()

    def resizeEvent(self, evt):
        boxHeight = 60
        self.buttonBox.setGeometry(
                0 if self.width() <= self.bgimage.width()
                    else (self.width() - self.bgimage.width()) / 2,
                min(self.bgimage.height()
                        - boxHeight
                        + (self.height() - self.bgimage.height()) / 2,
                    self.height() - boxHeight),
                min(self.width(), self.bgimage.width()),
                boxHeight
                )

    def paintEvent(self, evt):
        painter = QPainter(self)
        painter.drawPixmap(
                0 if self.width() <= self.bgimage.width()
                    else (self.width() - self.bgimage.width()) / 2,
                0 if self.height() <= self.bgimage.height()
                    else (self.height() - self.bgimage.height()) / 2,
                self.bgimage
                )


__all__ = ["LoaderWindow"]
