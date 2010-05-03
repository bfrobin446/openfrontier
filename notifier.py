from PyQt4.QtCore import *

class Notifier(QObject):
    def __init__(self, *args):
        QObject.__init__(self, *args)

    triggered = pyqtSignal()

    def trigger(self):
        self.triggered.emit()
