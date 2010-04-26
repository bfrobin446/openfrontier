#! /usr/bin/env python3

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import sys

app = QApplication(sys.argv)
app.setApplicationName("OpenFrontier")

import ui

ui.showMainWindow()
app.exec_()

# Let most of the GUI objects be garbage collected before the
# QApplication. Seems to save on segfaults.
del ui.mainWindow
