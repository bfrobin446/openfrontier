from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from collections import OrderedDict

from notifier import Notifier

changeNotifier = Notifier()

class Color(object):
    settings = QSettings()
    settings.beginGroup('colors')
    def __init__(self, name, default, dname):
        self.default = default
        self.name = name
        self.displayname = dname
        self.current = self.settings.value(self.name, self.default)
    def update(self, newColor):
        self.settings.setValue(self.name, newColor)
        self.current = newColor
        changeNotifier.trigger()

def defineColor(cat, name, default, dname):
    globals()[cat][name] = Color('/'.join((cat, name)), default, dname)

categories = ("galaxy", )
catnames   = ("Galaxy map", )
for cat in categories:
    globals()[cat] = OrderedDict()

defineColor('galaxy', 'background',  QColor(Qt.black), "Background")
defineColor('galaxy', 'text',        QColor(Qt.white), "Text")
defineColor('galaxy', 'solarsystem', QColor(Qt.white), "Solar system")
defineColor('galaxy', 'fleet',       QColor(Qt.blue),  "Ship or group of ships")
defineColor('galaxy', 'player',      QColor(Qt.cyan),  "Player fleet")
defineColor('galaxy', 'battle',      QColor(Qt.red),   "Ships - weapons fire detected")
defineColor('galaxy', 'sysbattle',   QColor("orange"), "Solar system - weapons fire detected")
