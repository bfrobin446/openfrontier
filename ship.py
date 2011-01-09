
class ShipClass:
    @classmethod
    def fromDOMElement(cls, element):
        sc = cls()
        sc.id = element.getAttribute("id")
        return sc
