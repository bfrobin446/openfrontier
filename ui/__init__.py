from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import openfrontier
import galaxymap
from location import Location

from .gamewindow import GameWindow

mainWindow = None

def showMainWindow():
    global mainWindow
    mainWindow = GameWindow()
    mainWindow.show()

def displayLocation(loc):
    if loc.locType == Location.ON_GALAXY_MAP:
        mainWindow.setCentralWidget(QGraphicsView(galaxymap.mainScene))

def customizeNewGame():
    pass
