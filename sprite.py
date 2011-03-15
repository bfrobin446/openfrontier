import os

from PyQt4.QtCore import *
from PyQt4.QtGui  import *

from domhelpers   import *

class Sprite:
    pass

class ShipSprite(Sprite):
    def __init__(self, spriteElement, imagesDir):
        self.headingStep = int(
                getFirstChildElementWithTagName(spriteElement,
                    "renderOptions").getAttribute("headingStep"))
        self.params = list(
                e.getAttribute("name")
                for e in getChildElementsWithTagName(spriteElement, 'param')
                )
        self.params.sort()
        self.bounds = {
                e.getAttribute("name"):
                    (int(e.getAttribute("min")), int(e.getAttribute("max")))
                for e in getChildElementsWithTagName(spriteElement, 'param')
                }
        self.images = {}
        for where, subdirs, files in os.walk(imagesDir):
            for f in files:
                img = QImage(os.path.join(where, f)).convertToFormat(
                        QImage.Format_ARGB32_Premultiplied)
                key = os.path.join(
                        os.path.relpath(where, imagesDir),
                        os.path.splitext(f)[0])
                pBits = img.bits()
                pBits.setsize(img.byteCount())
                self.images[key] = bytes(pBits)

        
