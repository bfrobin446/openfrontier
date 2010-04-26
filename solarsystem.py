from PyQt4.QtCore import *
from PyQt4.QtGui  import *

import domhelpers

class SolarSystem(object):
    @classmethod
    def fromDOMElement(cls, element):
        ss = cls()
        ss.id = element.getAttribute("id")
        coordsElement = domhelpers.getFirstChildElementWithTagName(element, "coords")
        ss.coords = QPointF(
                float(coordsElement.getAttribute('x')),
                float(coordsElement.getAttribute('y')) )
        ss.displayName = domhelpers.getInnerText(
                domhelpers.getFirstChildElementWithTagName(element, 'displayname') )
        return ss
