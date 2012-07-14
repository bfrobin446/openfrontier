'''
OpenFrontier global state

Important data members
----------------------
distPath
  Absolute path to the OpenFrontier distribution
defaultSavePath
  Default location for saved games
'''
import sys
import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

distPath = os.path.abspath(sys.path[0])

def distFile(relpath):
    '''Return ``relpath`` resolved relative to ``distPath``'''
    return os.path.join(distPath, os.path.normpath(relpath))

# TODO something appropriate and platform specific
defaultSavePath = distFile("SavedGames")

__all__ = ["distPath", "distFile", "defaultSavePath"]
