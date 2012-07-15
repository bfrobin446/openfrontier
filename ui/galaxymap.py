'''
Interactive galaxy map view/controller for OFWorld
'''
from PyQt4.QtCore import *
from PyQt4.QtGui  import *
from PyQt4        import uic

from ui import colors
import openfrontier

class MapWindow(QMainWindow):
    def __init__(self, world, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.world = world
        self.mapScene = MapScene(self.world)
        self.mapView = QGraphicsView(self.mapScene)
        uic.loadUi(openfrontier.distFile('ui/gamewindow.ui'), self)
        self.setCentralWidget(self.mapView)

    aboutToClose = pyqtSignal()

    def closeEvent(self, evt):
        self.aboutToClose.emit()
        evt.accept()

class MapScene(QGraphicsScene):
    def __init__(self, world, *args):
        QGraphicsScene.__init__(self, -512, -512, 1024, 1024, *args)
        self.world = world

        for ss in self.world.systems.values():
            self.addItem(SolarSystemMapItem(ss))

#~         self.timer = QTimer(self)
#~         self.timer.setInterval(50)
#~         self.timer.timeout.connect(self.tick)
#~         self.waiting = False
        self.setBackgroundBrush(colors.galaxy["background"].current)
        colors.changeNotifier.triggered.connect(self.updateColors)

#     def mousePressEvent(self, evt):
#        itemsHere = [i for i in self.items(evt.scenePos()) if i is not self.playerFleetItem]
#        if len(itemsHere) == 0:
#            setPlayerDestination(evt.scenePos())
#        elif len(itemsHere) == 1:
#            setPlayerDestination(itemsHere[0].worldObj())
#        else:
#            print("TODO menu")
# 
#     def startAnimation(self):
#         print("GalaxyMapScene.startAnimation()")
#         self.timer.start()
#     def stopAnimation(self):
#         print("GalaxyMapScene.stopAnimation()")
#         self.timer.stop()
# 
#     def tick(self):
#         #print "GalaxyMapScene.tick()"
#         QGraphicsScene.advance(self)
#         if not (self.playerFleetItem.wantAnimation() or self.waiting):
#             self.stopAnimation()

    def updateColors(self):
        self.setBackgroundBrush(colors.galaxy["background"].current)
        for item in self.items():
            try:
                item.updateColor()
            except AttributeError:
                pass

class MapItem(QAbstractGraphicsShapeItem):
    def __init__(self, center, radius = 8):
        QAbstractGraphicsShapeItem.__init__(self)
        self.setPos(center)
        self.setAcceptHoverEvents(True)
        self.hoverTextItem = QGraphicsSimpleTextItem(self)
        self.hoverTextItem.hide()
        self.staticTextItem = QGraphicsSimpleTextItem(self)
        self.setRadius(radius)
        self.updateColor() # subclasses should extend

    def setRadius(self, radius):
        self.radius = radius
        self.staticTextItem.setPos(radius + 5, -10)
        self.hoverTextItem.setPos(radius + 5, 8)

    def setColor(self, color):
        self.setPen(QPen(QBrush(color), 3))

    def updateColor(self):
        self.staticTextItem.setBrush(QBrush(colors.galaxy["text"].current))
        self.hoverTextItem.setBrush(QBrush(colors.galaxy["text"].current))

    def setHoverText(self, text):
        self.hoverTextItem.setText(text)

    def setStaticText(self, text):
        self.staticTextItem.setText(text)

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
        self.setStaticText(ss.displayName)

    def updateColor(self):
        super().updateColor()
        self.setColor(colors.galaxy['solarsystem'].current)

# class FleetMapItem(MapItem):
#     def __init__(self, fleet):
#         MapItem.__init__(self, fleet.location.coords, 8)
#         self.fleet = fleet
# 
#     def location(self):
#         return self.fleet.location
# 
#     def advance(self, phase):
#         if phase == 0:
#             if self.fleet.navigator is not None:
#                 self.fleet.navigator.update(self.fleet, [])
#         else:
#             self.fleet.move()
#             if self.fleet.location.locType == Location.ON_GALAXY_MAP:
#                 self.setPos(self.fleet.location.coords)
#             else:
#                 self.scene().removeItem(self)
# 
#     def updateColor(self):
#         MapItem.updateColor(self)
#         self.setColor(colors.galaxy["fleet"].current)
# 
# class PlayerFleetMapItem(FleetMapItem):
#     def __init__(self, fleet):
#         FleetMapItem.__init__(self, fleet)
#     def wantAnimation(self):
#         return self.fleet.navigator.destination is not None
#     def updateColor(self):
#         # override FleetMapItem.updateColor(); extend MapItem.updateColor()
#         MapItem.updateColor(self)
#         self.setColor(colors.galaxy["player"].current)

#~ def populate():
#~     global mainScene
#~     if mainScene is None:
#~         mainScene = GalaxyMapScene(-512, -512, 1024, 1024)
#~     else:
#~         mainScene.clear()
#~ 
#~     for ss in openfrontier.solarSystems.values():
#~         mainScene.addSolarSystem(ss)
#~ 
#~     for fleet in openfrontier.activeFleets:
#~         if Location.ON_GALAXY_MAP == fleet.location.locType:
#~             mainScene.addFleet(fleet)
#~ 
#~ def setPlayerDestination(dest):
#~     print("setPlayerDestination(", dest, ")")
#~     openfrontier.player.setDestination(dest)
#~     #TODO ensure course line visible
#~     mainScene.startAnimation()
