from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import itertools

from .colorbutton import ColorButton
from . import colors

class PrefsDialog(QDialog):
    def __init__(self, parent=None, flags=Qt.Widget):
        QDialog.__init__(self, parent, flags)
        self.settings = QSettings()
        self.setLayout(QVBoxLayout(self))

        self.tabs = QTabWidget(self)
        self.layout().addWidget(self.tabs)

        self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.RestoreDefaults,
                accepted = self.close
                )
        self.layout().addWidget(self.buttons)

        self.buttons.button(self.buttons.RestoreDefaults).clicked.connect(self.defaults)

        self.addTab(ColorPrefPane(), "Colors")

    def addTab(self, widget, title):
        scroller = QScrollArea()
        scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroller.setWidget(widget)
        scroller.setMinimumWidth(widget.sizeHint().width() +
                qApp.style().pixelMetric(QStyle.PM_ScrollBarExtent, None, scroller) * 2)
        widget.resize(widget.sizeHint())
        self.tabs.addTab(scroller, title)

    def defaults(self):
        self.tabs.currentWidget().widget().defaults()

class ColorPrefPane(QWidget):
    def __init__(self, parent=None, flags=Qt.Widget):
        QWidget.__init__(self, parent, flags)
        self.setLayout(QVBoxLayout(self))
        for cat, catname in zip(colors.categories, colors.catnames):
            self.layout().addWidget(QLabel(''.join(('<b><big>', catname, '</big></b>')), self))
            catLayout = QGridLayout()
            self.layout().addLayout(catLayout)
            for i, c in enumerate(getattr(colors, cat).values()):
                catLayout.addWidget(QLabel(c.displayname, self), i, 1)
                picker = ColorButton(c.current, self, colorChanged = c.update)
                catLayout.addWidget(picker, i, 0)

    def defaults(self):
        for color, picker in zip(
                itertools.chain.from_iterable(
                    getattr(colors, cat).values() for cat in colors.categories),
                (obj for obj in self.children() if isinstance(obj, ColorButton))
                ):
            picker.setColor(color.default)
