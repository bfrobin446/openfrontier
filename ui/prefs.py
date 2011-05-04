from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import itertools

from .            import colors
from .            import keys
from .colorbutton import ColorButton


class KeyPicker(QLineEdit):
    keyChanged = pyqtSignal(Qt.Key)

    def __init__(self, key=None, parent=None, flags=Qt.Widget, **kwargs):
        QLineEdit.__init__(self, parent, **kwargs)
        self.setWindowFlags(flags)
        self.setReadOnly(True)
        self.key = key
        self.setText(self.textForKey(self.key))

    @staticmethod
    def textForKey(k):
        for name, value in Qt.__dict__.items():
            if name[0:4] == 'Key_':
                if k == value:
                    return name
        return ''

    def focusInEvent(self, evt):
        self.setText("<press a key>")

    def keyPressEvent(self, evt):
        self.key = evt.key()
        self.setText(self.textForKey(self.key))
        self.keyChanged.emit(self.key)

    def setKey(self, key):
        self.key = key
        self.setText(self.textForKey(self.key))
        self.keyChanged.emit(self.key)


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

        self.buttons.button(
                self.buttons.RestoreDefaults).clicked.connect(self.defaults)

        self.addTab(ColorPrefPane(), "Colors")
        self.addTab(KeyPrefPane(), "Keys")

    def addTab(self, widget, title):
        scroller = QScrollArea()
        scroller.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroller.setWidget(widget)
        scroller.setMinimumWidth(
                widget.sizeHint().width()
                + qApp.style().pixelMetric(
                    QStyle.PM_ScrollBarExtent, None, scroller)
                * 2)
        widget.resize(widget.sizeHint())
        self.tabs.addTab(scroller, title)

    def defaults(self):
        self.tabs.currentWidget().widget().defaults()


class ColorPrefPane(QWidget):
    def __init__(self, parent=None, flags=Qt.Widget):
        QWidget.__init__(self, parent, flags)
        self.setLayout(QVBoxLayout(self))
        for cat, catname in zip(colors.categories, colors.catnames):
            self.layout().addWidget(
                    QLabel(''.join(('<b><big>', catname, '</big></b>')), self))
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


class KeyPrefPane(QWidget):
    def __init__(self, parent=None, flags=Qt.Widget):
        QWidget.__init__(self, parent, flags)
        self.setLayout(QVBoxLayout(self))
        for cat, catname in zip(keys.categories, keys.catnames):
            self.layout().addWidget(
                    QLabel(''.join(('<b><big>', catname, '</big></b>')), self))
            catLayout = QGridLayout()
            self.layout().addLayout(catLayout)
            for i, c in enumerate(getattr(keys, cat).values()):
                catLayout.addWidget(QLabel(c.displayname, self), i, 1)
                picker = KeyPicker(c.current, self, keyChanged = c.update)
                catLayout.addWidget(picker, i, 0)

    def defaults(self):
        for key, picker in zip(
                itertools.chain.from_iterable(
                    getattr(keys, cat).values() for cat in keys.categories),
                (obj for obj in self.children() if isinstance(obj, KeyPicker))
                ):
            picker.setKey(key.default)
