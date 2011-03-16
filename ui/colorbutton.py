from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import operator
from functools import reduce

class ColorButton(QAbstractButton):
    colorChanged = pyqtSignal(QColor)

    def color(self):
        return self.currentColor

    def setColor(self, newColor):
        self.currentColor = newColor
        self.colorChanged.emit(newColor)
        self.update()

    color = property(color, setColor)

    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], QColor):
            QAbstractButton.__init__(self, *args[1:], **kwargs)
            self.currentColor = args[0]
        else:
            QAbstractButton.__init__(self, *args, **kwargs)
            self.currentColor = QColor(Qt.black)

        self.setSizePolicy(QSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Minimum, QSizePolicy.ToolButton))

        self.margins = self.sizeHint() - QSize(22, 22)
        self.clicked.connect(self.onClick)

    def onClick(self):
        self.currentColor = QColorDialog.getColor(self.currentColor, self)
        self.colorChanged.emit(self.currentColor)

    def initStyleOption(self, option):
        option.initFrom(self)
        option.toolButtonStyle = Qt.ToolButtonIconOnly
        option.features = option.ToolButtonFeatures(0)
                                    #QStyleOptionToolButton.None
        option.subControls = QStyle.SC_ToolButton
        option.activeSubControls = (
                QStyle.SC_ToolButton if self.isDown() else QStyle.SC_None)
        option.state = reduce(operator.or_, (
            QStyle.State_Active
                if self.isActiveWindow() else QStyle.State_None,

            QStyle.State_Enabled
                if self.isEnabled()      else QStyle.State_None,

            QStyle.State_HasFocus
                if self.hasFocus()       else QStyle.State_None,

            QStyle.State_Sunken
                if self.isDown()         else QStyle.State_Raised,
            ))

    def sizeHint(self):
        option = QStyleOptionToolButton()
        self.initStyleOption(option)
        return qApp.style().sizeFromContents(
                QStyle.CT_ToolButton, option, QSize(22, 22), self)
    
    def paintEvent(self, evt):
        option = QStyleOptionToolButton()
        self.initStyleOption(option)

        painter = QStylePainter(self)
        painter.drawComplexControl(QStyle.CC_ToolButton, option)

        contentsSize = self.size() - self.margins
        contentsRect = QRect(
                QPoint(
                    self.margins.width()  / 2,
                    self.margins.height() / 2
                    ),
                contentsSize
                )
        painter.fillRect(contentsRect, self.currentColor)

        frameOption = QStyleOptionFrame()
        frameOption.initFrom(self)
        frameOption.rect = contentsRect
        painter.drawPrimitive(QStyle.PE_Frame, frameOption)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    widget = QWidget()
    widget.setLayout(QHBoxLayout(widget))
    button = ColorButton(widget)
    widget.layout().addWidget(button)
    widget.show()
    app.exec_()
