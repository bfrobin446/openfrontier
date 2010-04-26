from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from collections import OrderedDict

class Key(object):
    settings = QSettings()
    settings.beginGroup('keys')
    def __init__(self, name, default, displayname):
        self.default = default
        self.name = name
        self.displayname = displayname
        self.current = self.settings.value(self.name, self.default)

def defineKey(category, name, default, displayname):
    globals()[category][name] = Key('/'.join((category, name)), default, displayname)

categories = ("galaxy", )
for cat in categories:
    globals()[cat] = OrderedDict()

defineKey("galaxy", "wait", Qt.Key_Space, "Cancel destination / Wait")
