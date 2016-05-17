'''
OpenFrontier global state

Important data members
----------------------
activeWorld
  World object in use, or None if no game is loaded.
defaultSavePath
  Default location for saved games
distPath
  Absolute path to the OpenFrontier distribution
PICKLE_VERSION
  Magic number to detect save/load incompatibility
'''
import sys
import os.path

PICKLE_VERSION = 1

distPath = os.path.abspath(sys.path[0])

def distFile(relpath):
    '''Return ``relpath`` resolved relative to ``distPath``'''
    return os.path.join(distPath, os.path.normpath(relpath))

# TODO something appropriate and platform specific
defaultSavePath = distFile("SavedGames")

activeWorld = None
