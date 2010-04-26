from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from location import Location
from ui import colors
import openfrontier

mainScene = None

class GalaxyMapScene(QGraphicsScene):
    def __init__(self, *args):
        QGraphicsScene.__init__(self, *args)
        self.timer = QTimer(self)
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.tick)
        self.waiting = False

    def addFleet(self, fleet):
        if fleet is openfrontier.player.fleet:
            self.playerFleetItem = PlayerFleetMapItem(fleet)
            self.addItem(self.playerFleetItem)
        else:
            self.addItem(FleetMapItem(fleet))

    def addSolarSystem(self, ss):
        self.addItem(SolarSystemMapItem(ss))

    def clear(self):
        self.playerFleetItem = None
        QGraphicsScene.clear(self)

    def mousePressEvent(self, evt):
       itemsHere = [i for i in self.items(evt.scenePos()) if i is not self.playerFleetItem]
       if len(itemsHere) == 0:
           setPlayerDestination(Location(Location.ON_GALAXY_MAP, coords=evt.scenePos()))
       elif len(itemsHere) == 1:
           setPlayerDestination(itemsHere[0].location())
       else:
           print("TODO menu")

    def startAnimation(self):
        print("GalaxyMapScene.startAnimation()")
        self.timer.start()
    def stopAnimation(self):
        print("GalaxyMapScene.stopAnimation()")
        self.timer.stop()

    def tick(self):
        #print "GalaxyMapScene.tick()"
        QGraphicsScene.advance(self)
        if not (self.playerFleetItem.wantAnimation() or self.waiting):
            self.stopAnimation()

class MapItem(QAbstractGraphicsShapeItem):
    def __init__(self, center, radius = 12):
        QAbstractGraphicsShapeItem.__init__(self)
        self.setPos(center)
        self.setAcceptHoverEvents(True)
        self.hoverTextItem = QGraphicsSimpleTextItem(self)
        self.hoverTextItem.setBrush(QBrush(Qt.white))
        self.hoverTextItem.hide()
        self.setRadius(radius)

    def setRadius(self, radius):
        self.radius = radius
        self.hoverTextItem.setPos(radius + 5, -10)

    def setHoverText(self, text):
        self.hoverTextItem.setText(text)

    def boundingRect(self):
        radius = self.radius
        return QRectF(-(radius + 2), -(radius + 2), 2 * (radius + 2), 2 * (radius + 2))

    def paint(self, painter, options, widget=None):
        painter.setPen(self.pen())
        painter.drawEllipse(QPointF(0,0), self.radius, self.radius)

    def hoverEnterEvent(self, evt):
        self.hoverTextItem.show()

    def hoverLeaveEvent(self, evt):
        self.hoverTextItem.hide()

class SolarSystemMapItem(MapItem):
    def __init__(self, ss):
        MapItem.__init__(self, ss.coords)
        self.system = ss
        self.setPen(QPen(QBrush(colors.galaxy["solarsystem"].current), 3))
        self.setHoverText(ss.displayName)

    def location(self):
        return Location(Location.ON_SYSTEM_MAP, self.system)

class FleetMapItem(MapItem):
    def __init__(self, fleet):
        MapItem.__init__(self, fleet.location.coords, 8)
        self.fleet = fleet
        self.setPen(QPen(QBrush(colors.galaxy["fleet"].current), 3))

    def location(self):
        return self.fleet.location

    def advance(self, phase):
        if phase == 0:
            if self.fleet.navigator is not None:
                self.fleet.navigator.update(self.fleet, [])
        else:
            self.fleet.move()
            if self.fleet.location.locType == Location.ON_GALAXY_MAP:
                self.setPos(self.fleet.location.coords)
            else:
                self.scene().removeItem(self)

class PlayerFleetMapItem(FleetMapItem):
    def __init__(self, fleet):
        FleetMapItem.__init__(self, fleet)
        self.setPen(QPen(QBrush(colors.galaxy["player"].current), 3))
    def wantAnimation(self):
        return self.fleet.navigator.destination is not None

def populate():
    global mainScene
    if mainScene is None:
        mainScene = GalaxyMapScene(-512, -512, 1024, 1024)
        mainScene.setBackgroundBrush(colors.galaxy["background"].current)
    else:
        mainScene.clear()

    for ss in openfrontier.solarSystems.values():
        mainScene.addSolarSystem(ss)

    for fleet in openfrontier.activeFleets:
        if Location.ON_GALAXY_MAP == fleet.location.locType:
            mainScene.addFleet(fleet)

def setPlayerDestination(dest):
    print("setPlayerDestination(", dest, ")")
    openfrontier.player.setDestination(dest)
    #TODO ensure course line visible
    mainScene.startAnimation()
