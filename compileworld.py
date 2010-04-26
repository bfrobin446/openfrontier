#! /usr/bin/env python3

import itertools
import os.path
import sys
import textwrap

from decimal import Decimal
from pickle  import Pickler
from xml.dom import minidom

from domhelpers  import *
from fleet       import *
from location    import Location
from player      import Player
from solarsystem import SolarSystem

worlddir = sys.argv[1]

xmlFile = open(os.path.join(worlddir, 'data.xml'))
pickleFile = open(os.path.join(worlddir, 'data.pickle'), 'wb')
codeFile = open(os.path.join(worlddir, 'ofworld.py'), 'w')

xmlDocument = minidom.parse(xmlFile)
xmlFile.close()

pickler = Pickler(pickleFile, protocol=0)
pickler.dump(0)
pickler.dump('')

# Technologies
techs = {}
#TODO parse techs
pickler.dump(techs)

# Ship classes
shipClasses = {}
for element in xmlDocument.getElementsByTagName("shipclass"):
    pass
pickler.dump(shipClasses)

fleetTemplates = {}
for element in xmlDocument.getElementsByTagName("fleettemplate"):
    pass
pickler.dump(fleetTemplates)

solarSystems = {}
for element in xmlDocument.getElementsByTagName("solarsystem"):
    ss = SolarSystem.fromDOMElement(element)
    solarSystems[ss.id] = ss
pickler.dump(solarSystems)

dateElem = getFirstChildElementWithTagName(xmlDocument.documentElement, 'date')
date = Decimal(getInnerText(dateElem))
pickler.dump(date)

fleets = []
for element in xmlDocument.getElementsByTagName("fleet"):
    if element.parentNode is xmlDocument.documentElement:
        fleets.append(fleetFromElement(element))
pickler.dump(fleets)

playerElements = xmlDocument.getElementsByTagName("player")
if len(playerElements) == 1:
    pickler.dump(Player.fromDOMElement(playerElements[0]))
else:
    pickler.dump([Player.fromDOMElement(e) for e in playerElements])

pickleFile.close()

for element in xmlDocument.getElementsByTagName("code"):
    print(textwrap.dedent(getInnerText(element)).strip(), file=codeFile)

codeFile.close()
