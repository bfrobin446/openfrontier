from PyQt4.QtCore import QPointF

class SolarSystem:
    '''A solar system in the game world.

    Important data members
    ----------------------
    id
      String uniquely identifying this ``SolarSystem``
    coords
      System's location on the galaxy map as ``QPointF``
    displayName
      Name displayed to the player, which need not be unique
    '''

    @classmethod
    def fromDOMElement(cls, element):
        import domhelpers
        ss = cls()
        ss.id = element.getAttribute("id")
        coordsElement = domhelpers.getFirstChildElementWithTagName(element, "coords")
        ss.coords = QPointF(
                float(coordsElement.getAttribute('x')),
                float(coordsElement.getAttribute('y')) )
        ss.displayName = domhelpers.getInnerText(
                domhelpers.getFirstChildElementWithTagName(element, 'displayname') )
        return ss
