import sys

import domhelpers

class ShipClass:
    @classmethod
    def fromDOMElement(cls, element):
        sc = cls()
        sc.id = element.getAttribute("id")
        sc.sprite = domhelpers.getFirstChildElementWithTagName(
                element, "sprite").getAttribute("name")
        sc.cruiseSpeed = float(
                domhelpers.getFirstChildElementWithTagName(
                    element, "warp").getAttribute("cruise"))
        sc.dashSpeed = float(
                domhelpers.getFirstChildElementWithTagName(
                    element, "warp").getAttribute("dash"))
        return sc

class Ship:
    @classmethod
    def fromDOMElement(cls, element):
        s = cls()
        try:
            main = sys.modules["__main__"]
            s.class_ = main.shipClasses[element.getAttribute("class")]
        except KeyError:
            raise
        return s

    @property
    def warpSpeed(self):
        try:
            return self.cruiseSpeed
        except AttributeError:
            return self.class_.cruiseSpeed
