import math
from naca5305 import naca5305
from scale import scaleListOfTuple
from fattenTe import fattenTe
#from dumpAttr import dumpAttr
#from verticesAsList import verticesAsList

import cadquery as cq # type: ignore

from typing import List, Sequence, Tuple

X = 0
Y = 1
Z = 2

dihederal = math.radians(5)
sweep = math.radians(0)
h: float = 100
chord: float = 50 
wingThickness: float = 0.20
ribThickness: float = wingThickness

def show(o: object):
    if 'show_object' in globals():
        show_object(o)

def dbg(*args):
    if 'log' in globals():
        log(*args)
    else:
        print(*args)

# Normalize, Scale, fattenTe
scaleFactor: float = 1/naca5305[0][0]
nNaca5305 = scaleListOfTuple(naca5305, scaleFactor)
sNaca5305: List[Tuple[float, float]] = scaleListOfTuple(nNaca5305, chord)
fNaca5305: List[Tuple[float, float]] = fattenTe(sNaca5305, wingThickness, 10)


airfoil = (
    cq.Workplane("YZ")
    .polyline(fNaca5305).close()
)
dbg(f'airfoil.val().isValid()={airfoil.val().isValid()}')
#show(airfoil)

halfWing = (
    airfoil
    .sweep(
        cq.Workplane("YX")
        .spline([(0, 0, 0), (h * math.sin(sweep), h, h * math.sin(-dihederal))])
    )
)
dbg(f'halfWing.val().isValid()={halfWing.val().isValid()}')
#show(halfWing)

# Shell the halfWing
#halfWingShell = halfWing.shell(-0.25)
#show(halfWingShell)


halfWingBb = halfWing.val().BoundingBox()
dbg(f'ylen={halfWingBb.ylen}, zlen={halfWingBb.zlen}')

# Create the braces which the ribs will be cut from 
braceCount = 8
braceGap: float = h / (braceCount-1)
bracePlates = []
for i in range(0, braceCount):
    ribXPos = i * braceGap
    if i == (braceCount - 1):
        ribXPos -= ribThickness
    bracePlate = (
        cq.Workplane("YZ", origin=(ribXPos, (halfWingBb.ylen)/2, halfWingBb.zlen/2))
        .rect(halfWingBb.ylen * 1.10, halfWingBb.zlen * 1.50)
        # First rib is 1/2 thickness
        .extrude(ribThickness if i != 0 else ribThickness / 2)
    )
    #dbg(f'{i}: braceGap={braceGap} bracePlate.val().isValid()={bracePlate.val().isValid()}')
    bracePlates.append(bracePlate)
    #show(bracePlate)

# Create the ribs
ribs = [plate.intersect(halfWing) for plate in bracePlates]
#for rib in ribs: show(rib)

halfWingCutter = (
    cq.Workplane("YZ")
    .polyline(fNaca5305).close()
    .offset2D(-wingThickness, 'intersection')
    .sweep(
        cq.Workplane("YX")
        .spline([(0, 0, 0), (h * math.sin(sweep), h, h * math.sin(-dihederal))])
    )
)
#show(halfWingCutter)

# Cut out the center of the halfWing
halfWingHollow = halfWing.cut(halfWingCutter)
#show(halfWingHollow)

# Union the ribs and wing
halfWingWithRibs = halfWingHollow
for rib in ribs:
    halfWingWithRibs = halfWingWithRibs.union(rib)
#show(halfWingWithRibs)

fullWing = halfWingWithRibs.mirror("YZ").union(halfWingWithRibs)
dbg(f'fullWing.val().isValid()={fullWing.val().isValid()}')
#show(fullWing)

verticalWing = fullWing.rotate((0, 0, 0), (1, 0, 0), -90)
dbg(f'verticalWing.val().isValid()={verticalWing.val().isValid()}')
#show(verticalWing)

wing4 = verticalWing.translate((0, 0, fNaca5305[-1][X] + (h * math.sin(sweep))))
dbg(f'wing4.val().isValid()={wing4.val().isValid()}')
show(wing4)

import io
tolerance=0.001;
f = io.open(f'wing4-tol_{tolerance}-tk_{wingThickness}.stl', 'w+')
cq.exporters.exportShape(wing4, cq.exporters.ExportTypes.STL, f, tolerance)
f.close()
