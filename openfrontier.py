import sys
import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from PyQt4 import uic

import galaxymap
import ui

def loadGame(sourcePath, shouldStart = True):
    global savedGamePath
    savedGamePath = sourcePath

    from pickle import Unpickler
    with open(sourcePath, 'rb') as f:
        unpickler = Unpickler(f)

        formatVersion = unpickler.load()
        if formatVersion > 0:
            raise ValueError("Unsupported pickle version " + str(formatVersion))

        global worldDir
        worldDir = unpickler.load()
        if not worldDir:
            worldDir = os.path.dirname(sourcePath)
        print("Looking for ofworld in", worldDir, file=sys.stderr)
        sys.path[0:0] = ( worldDir, )
        global ofworld
        if 'ofworld' in sys.modules:
            del sys.modules['ofworld']
            del ofworld
        import ofworld
        del sys.path[0]

        global technologies
        technologies = unpickler.load()

        global shipClasses
        shipClasses = unpickler.load()

        global fleetTemplates
        fleetTemplates = unpickler.load()

        global solarSystems
        solarSystems = unpickler.load()

        global currentDate
        currentDate = unpickler.load()

        global activeFleets
        activeFleets = unpickler.load()

        global player
        player = unpickler.load()

    if shouldStart:
        startGame()

def newGame(sourceDir):
    loadGame(os.path.join(sourceDir, 'data.pickle'), False)
    try:
        ofworld.customizeNewGame()
    except (NameError, AttributeError, TypeError):
        ui.customizeNewGame()
    
    if player.fleet not in activeFleets:
        activeFleets.append(player.fleet)

    startGame()

def startGame():
    galaxymap.populate()
    ui.displayLocation(player.fleet.location)

distPath = os.path.abspath(sys.path[0])

def distFile(relpath):
    return os.path.join(distPath, os.path.normpath(relpath))

# TODO something appropriate and platform specific
defaultSavePath = distFile("SavedGames")
