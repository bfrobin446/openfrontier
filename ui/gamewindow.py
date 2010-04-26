from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from PyQt4 import uic

import openfrontier

from .splash import SplashWidget
from .prefs  import PrefsDialog

class GameWindow(QMainWindow):
    def __init__(self, parent=None, flags=Qt.Widget):
        QMainWindow.__init__(self, parent, flags)
        uic.loadUi(openfrontier.distFile('ui/gamewindow.ui'), self)
        splash = SplashWidget(self)
        self.setCentralWidget(splash)

        self.actionNew.triggered.connect(self.new)
        splash.btnNewGame.clicked.connect(self.new)

        self.actionLoad.triggered.connect(self.open)
        splash.btnLoadGame.clicked.connect(self.open)

        self.actionQuit.triggered.connect(self.close)
        splash.btnQuit.clicked.connect(self.close)

        self.actionSettings.triggered.connect(self.showSettings)
        splash.btnSettings.clicked.connect(self.showSettings)

    def open(self):
        saveDir = QSettings().value("savedGameDir", openfrontier.defaultSavePath).toString()
        fileToLoad = QFileDialog.getOpenFileName(
                self,
                "Choose saved game to open",
                saveDir,
                "OpenFrontier saves (*.ofplt)")
        if fileToLoad:
            openfrontier.loadGame(fileToLoad)

    def new(self):
        worldDir = openfrontier.distFile('')
        worldToLoad = QFileDialog.getOpenFileName(
                self,
                "Choose world for new game",
                worldDir,
                "OpenFrontier worlds (*.ofworld)")
        if worldToLoad:
            openfrontier.newGame(worldToLoad)

    def showSettings(self):
        dlg = PrefsDialog(self)
        dlg.setWindowModality(Qt.WindowModal)
        dlg.show()
