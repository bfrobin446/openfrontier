#! /usr/bin/env python3

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import sys

app = QApplication(sys.argv)
app.setApplicationName("OpenFrontier")

import ui

initialWindow = ui.LoaderWindow()
initialWindow.show()
app.exec_()
