#! /usr/bin/env python3

import bz2
import os.path
import pickle
import shutil
import subprocess
import sys
import tempfile

from collections import OrderedDict
from xml.dom import minidom

import sprite

from domhelpers import *

ofBaseDir = sys.path[0]
ofPOVRayLibDir = os.path.join(ofBaseDir, 'povray')

def runPOVRayForShip(source, dest, imageSize, cameraRadius, cameraAngle,
        headingStep, freeParams, fixedParams=None, logFile=None):
    if logFile is None:
        logFile = sys.stderr
    if fixedParams is None:
        fixedParams = OrderedDict()
    if freeParams:
        remainingFreeParams = freeParams.copy()
        (pname, (pmin, pmax)) = remainingFreeParams.popitem()
        childFixedParams = fixedParams.copy()
        for i in range(pmin, pmax + 1):
            childFixedParams[pname] = i
            runPOVRayForShip(source, os.path.join(dest, pname, str(i)),
                imageSize, cameraRadius, cameraAngle, headingStep,
                remainingFreeParams, childFixedParams, logFile)
    else:
        os.makedirs(dest)
        for heading in range(0, 360, headingStep):
            command = [
                    "povray",
                    os.path.join(ofPOVRayLibDir, 'render.ini'),
                    "+L" + ofPOVRayLibDir,
                    "+L" + os.path.dirname(source),
                    "+I" + source,
                    "+O" + os.path.join(dest, str(heading)),
                    "+W"+imageSize, "+H"+imageSize,
                    "Declare=OF_Heading="+str(heading),
                    "Declare=OF_CameraRadius="+cameraRadius,
                    "Declare=OF_CameraAngle="+cameraAngle
                ] + [
                    "Declare=" + name + '=' + str(value)
                    for name, value in fixedParams.items()
                ]
            print(' '.join(command), file=logFile)
            logFile.flush()
            subprocess.call(command, stderr=logFile)

def renderSprite(sourceDir, destPath):
    xmlSource = os.path.join(sourceDir, 'sprite.xml')
    xmlDoc = minidom.parse(xmlSource)
    spriteElement=xmlDoc.documentElement
    spriteType = spriteElement.getAttribute("type")

    if spriteType == 'ship':
        renderShip(spriteElement, sourceDir, destPath)
    else:
        print("Sprite type", spriteType, "not supported", file=sys.stderr)

def renderShip(spriteElement, sourceDir, destPath):
    sourceElem = getFirstChildElementWithTagName(spriteElement, 'source')
    params = OrderedDict()
    for pe in getChildElementsWithTagName(spriteElement, 'param'):
        params[pe.getAttribute('name')] = (
                int(pe.getAttribute('min')), int(pe.getAttribute('max')))
    if sourceElem.getAttribute("type") == 'povray':
        optionsElem = getFirstChildElementWithTagName(
                spriteElement, 'renderOptions')
        imageSize = optionsElem.getAttribute('imageSize')
        cameraRadius = optionsElem.getAttribute('cameraRadius')
        cameraAngle = optionsElem.getAttribute('cameraAngle')
        headingStep = int(optionsElem.getAttribute('headingStep'))
        renderDir = tempfile.mkdtemp()
        print("renderDir:", renderDir, file=sys.stderr)
        runPOVRayForShip(
                os.path.join(sourceDir, getInnerText(sourceElem)),
                renderDir,
                imageSize, cameraRadius, cameraAngle, headingStep, params,
                logFile=open(destPath + '.log', 'w'))
        
        spriteObj = sprite.ShipSprite(spriteElement, renderDir)
        pickle.dump(
                spriteObj,
                bz2.BZ2File(
                    os.path.join(destPath,
                        os.path.basename(sourceDir) + '.ofsprite'),
                    'w')
                )
        shutil.rmtree(renderDir)

if __name__ == '__main__':
    sourceDir = sys.argv[1]
    destPath = sys.argv[2]
    renderSprite(sourceDir, destPath)
