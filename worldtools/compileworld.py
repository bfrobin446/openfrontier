#! /usr/bin/env python3

import errno
import itertools
import os.path
import sys
import textwrap

from decimal import Decimal
from pickle  import Pickler
from xml.dom import minidom

# We need to import some game classes from outside our subdirectory.
myPath = sys.path[0]
distPath = os.path.normpath(os.path.join(myPath, '..'))
sys.path.insert(0, distPath)

import openfrontier
import spritc

from domhelpers  import *
from ofworld     import OFWorld
from solarsystem import SolarSystem

def ensureDirs(*args, **kwargs):
    try:
        os.makedirs(*args, **kwargs)
    except os.error as e:
        if e.errno != errno.EEXIST:
            raise

srcPath = sys.argv[1]
destdir = sys.argv[2]

xmlFile = open(os.path.join(srcPath, 'data.xml'))
ensureDirs(destdir)
pickleFile = open(os.path.join(destdir, 'data.pickle'), 'wb')
codeFile = open(os.path.join(destdir, 'ofworld.py'), 'w')

xmlDocument = minidom.parse(xmlFile)
xmlFile.close()

pickler = Pickler(pickleFile, protocol=0)
pickler.dump(openfrontier.PICKLE_VERSION)

solarSystems = {}
for element in xmlDocument.getElementsByTagName("solarsystem"):
    ss = SolarSystem.fromDOMElement(element)
    solarSystems[ss.id] = ss

gameWorld = OFWorld()
gameWorld.systems = solarSystems

pickler.dump(gameWorld)

# # Technologies
# techs = {}
# #TODO parse techs
# pickler.dump(techs)
# 
# # Ship classes
# shipClasses = {}
# for element in xmlDocument.getElementsByTagName("shipclass"):
#     sc = ShipClass.fromDOMElement(element)
#     shipClasses[sc.id] = sc
# pickler.dump(shipClasses)
# 
# fleetTemplates = {}
# for element in xmlDocument.getElementsByTagName("fleettemplate"):
#     pass
# pickler.dump(fleetTemplates)
# 
# solarSystems = {}
# for element in xmlDocument.getElementsByTagName("solarsystem"):
#     ss = SolarSystem.fromDOMElement(element)
#     solarSystems[ss.id] = ss
# pickler.dump(solarSystems)
# 
# dateElem = getFirstChildElementWithTagName(xmlDocument.documentElement, 'date')
# date = Decimal(getInnerText(dateElem))
# pickler.dump(date)
# 
# fleets = []
# for element in xmlDocument.getElementsByTagName("fleet"):
#     if element.parentNode is xmlDocument.documentElement:
#         fleets.append(Fleet.fromDOMElement(element))
# pickler.dump(fleets)
# 
# playerElements = xmlDocument.getElementsByTagName("player")
# if len(playerElements) == 1:
#     pickler.dump(Player.fromDOMElement(playerElements[0]))
# else:
#     pickler.dump([Player.fromDOMElement(e) for e in playerElements])
# 
# pickleFile.close()
# 
# for element in xmlDocument.getElementsByTagName("code"):
#     print(textwrap.dedent(getInnerText(element)).strip(), file=codeFile)
# 
# codeFile.close()
# 
# spriteNames = set(elem.getAttribute("name")
#         for elem in xmlDocument.getElementsByTagName("sprite"))
# for s in spriteNames:
#     spriteSrcDir = os.path.join(srcPath, 'sprites', s)
#     spriteDestDir = os.path.join(destdir, 'sprites')
#     if not os.path.exists(
#             os.path.join(spriteDestDir, s + '.ofsprite')):
#         ensureDirs(spriteDestDir)
#         spritc.renderSprite(spriteSrcDir, spriteDestDir)
