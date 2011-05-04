from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from collections import OrderedDict

from notifier import Notifier

changeNotifier = Notifier()

class Key(object):
    settings = QSettings()
    settings.beginGroup('keys')
    
    def __init__(self, name, default, displayname):
        self.default = default
        self.name = name
        self.displayname = displayname
        self.current = self.settings.value(self.name, self.default)

    def update(self, newKey):
        self.settings.setValue(self.name, newKey)
        self.current = newKey
        changeNotifier.trigger()


def defineKey(category, name, default, displayname):
    globals()[category][name] = Key('/'.join((category, name)), default, displayname)

categories = ("galaxy", "tactical")
catnames   = ("Galaxy map", "Tactical view")
for cat in categories:
    globals()[cat] = OrderedDict()

defineKey("galaxy", "wait", Qt.Key_Space, "Cancel destination / Wait")
defineKey("galaxy", "dash", Qt.Key_Shift, "Use dash speed")

defineKey("tactical", "thrust", Qt.Key_Up, "Forward thrust")
defineKey("tactical", "steerLeft", Qt.Key_Left, "Turn left")
defineKey("tactical", "steerRight", Qt.Key_Right, "Turn right")
