from PyQt4.QtCore import *
from PyQt4.QtGui  import *

class Location(object):
    ON_GALAXY_MAP = 0
    ON_SYSTEM_MAP = 1
    LANDED = 2
    def __init__(self, locType = ON_GALAXY_MAP, locObject = None, coords=QPointF(0.0, 0.0)):
        self.locType = locType
        self.locObject = locObject
        self.coords = coords
    
    def globalCoords(self):
        if self.locType == self.ON_GALAXY_MAP:
            return self.coords
        elif self.locType == self.ON_SYSTEM_MAP:
            return self.locObject.coords

