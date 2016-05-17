from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import openfrontier

from location import Location
from ship     import *

__all__ = ["Fleet", "NavigatorBase", "PlayerFleetNavigator"]

# Fleet: a group of ships with a common destination
class Fleet(object):
    def __init__(self, where=None, ships=None, navigator=None):
        self.location = where if where is not None else Location()
        self.ships = ships if ships is not None else []
        self.navigator = navigator

        self.updateWarpSpeed()
    
    def updateWarpSpeed(self):
        try:
            self.warpSpeed = min(s.warpSpeed for s in self.ships)
        except ValueError:
            self.warpSpeed = 1.0
            print("Assuming speed %f for empty fleet" % self.warpSpeed)

    def move(self):
        if self.location.locType == Location.ON_GALAXY_MAP:
            self.location.coords += self.navigator.course.toPointF()

    @classmethod
    def fromDOMElement(cls, element, defaultNavigatorClass=lambda:None):
        import domhelpers
        navElement = domhelpers.getFirstChildElementWithTagName(
                element, "navigator")
        navigator = ( NavigatorBase.fromDOMElement(navElement)
                if navElement else defaultNavigatorClass() )
        ships = [Ship.fromDOMElement(e)
                for e in domhelpers.getChildElementsWithTagName(
                   element, "ship")]
        return cls(ships=ships, navigator=navigator)

class NavigatorBase(object):
    @classmethod
    def fromDOMElement(cls, element):
        className = element.getAttribute("class")
        return globals()[className].fromDOMElement(element)

class PlayerFleetNavigator(NavigatorBase):
    def __init__(self):
        self.destination = None # Should be a Location object if not None
        self.course = QVector2D()

    def setDestination(self, loc):
        self.destination = loc

    def update(self, myFleet, otherFleets):
        # print "PlayerFleetNavigator.update()"
        if self.destination is None:
            self.course = QVector2D()
        else:
            vectorToTarget = QVector2D(
                    self.destination.globalCoords() - myFleet.location.coords)
            if vectorToTarget.length() < myFleet.warpSpeed:
                self.course = vectorToTarget
                if self.destination.locType == Location.ON_GALAXY_MAP:
                    self.destination = None
            else:
                self.course = vectorToTarget.normalized() * myFleet.warpSpeed
