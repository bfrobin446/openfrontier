
from fleet import Fleet, PlayerFleetNavigator

class Player(object):
    def setDestination(self, dest):
        self.fleet.navigator.setDestination(dest)

    @classmethod
    def fromDOMElement(cls, e):
        import domhelpers
        p = cls()
        p.fleet = Fleet.fromDOMElement(
                domhelpers.getFirstChildElementWithTagName(e, 'fleet'),
                PlayerFleetNavigator)
        return p

