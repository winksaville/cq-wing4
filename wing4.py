import math
from naca5305 import naca5305
from scale import scaleListOfTuple
from fattenTe import fattenTe
#from dumpAttr import dumpAttr
#from verticesAsList import verticesAsList

from pprint import pprint
import cadquery as cq # type: ignore

from typing import List, Sequence, Tuple

X = 0
Y = 1
Z = 2
dihederal = math.radians(5)
sweep = math.radians(0)
h: float = 100
chord: float = 50 
wingThickness: float = 0.30
ribThickness: float = 0.30

# Normalize, Scale, fattenTe
scaleFactor: float = 1/naca5305[0][0]
nNaca5305 = scaleListOfTuple(naca5305, scaleFactor)
sNaca5305: List[Tuple[float, float]] = scaleListOfTuple(nNaca5305, chord)
fNaca5305: List[Tuple[float, float]] = fattenTe(sNaca5305, 0.30, 10)


airfoil = (
    cq.Workplane("YZ")
    .polyline(fNaca5305).close()
)
log(f'airfoil.val().isValid()={airfoil.val().isValid()}')
#show_object(airfoil)

halfWing = (
    airfoil
    #.extrude(h)
    .sweep(
        cq.Workplane("YX")
        .spline([(0, 0, 0), (h * math.sin(sweep), h, h * math.sin(-dihederal))])
        #.spline([(0, 0, 0), (0, h, h * math.sin(-dihederal))])
    )
)
log(f'halfWing.val().isValid()={halfWing.val().isValid()}')
#show_object(halfWing)

# Shell the halfWing
#halfWingShell = halfWing.shell(-0.25)
#show_object(halfWingShell)


halfWingBb = halfWing.val().BoundingBox()
print(f'ylen={halfWingBb.ylen}, zlen={halfWingBb.zlen}')

# Create the braces which the ribs will be cut from 
braceCount = 8
braceGap: float = (h - ribThickness) / (braceCount-1)
bracePlates = []
for i in range(0, braceCount):
    bracePlate = (
        cq.Workplane("YZ", origin=(i * braceGap, (halfWingBb.ylen)/2, halfWingBb.zlen/2))
        .rect(halfWingBb.ylen * 1.10, halfWingBb.zlen * 1.50)
        # First rib is 1/2 thickness
        .extrude(ribThickness if i != 0 else ribThickness / 2)
    )
    #log(f'{i}: braceGap={braceGap} bracePlate.val().isValid()={bracePlate.val().isValid()}')
    bracePlates.append(bracePlate)
    #show_object(bracePlate)

# Create the ribs
ribs = [plate.intersect(halfWing) for plate in bracePlates]
#for rib in ribs:
#    show_object(rib)

halfWingCutter = (
    cq.Workplane("YZ")
    .polyline(fNaca5305).close()
    .offset2D(-wingThickness, 'intersection')
    #.extrude(h)
    .sweep(
        cq.Workplane("YX")
        .spline([(0, 0, 0), (h * math.sin(sweep), h, h * math.sin(-dihederal))])
        #.spline([(0, 0, 0), (0, h, h * math.sin(-dihederal))])
    )
)
#show_object(halfWingCutter)

# Cut out the center of the halfWing
halfWingHollow = halfWing.cut(halfWingCutter)
#show_object(halfWingHollow)

# Union the ribs and wing
halfWingWithRibs = halfWingHollow
for rib in ribs:
    halfWingWithRibs = halfWingWithRibs.union(rib)
#show_object(halfWingWithRibs)

fullWing = halfWingWithRibs.mirror("YZ").union(halfWingWithRibs)
log(f'fullWing.val().isValid()={fullWing.val().isValid()}')
#show_object(fullWing)

verticalWing = fullWing.rotate((0, 0, 0), (1, 0, 0), -90)
log(f'verticalWing.val().isValid()={verticalWing.val().isValid()}')
#show_object(verticalWing)

wing4 = verticalWing.translate((0, 0, fNaca5305[-1][X] + (h * math.sin(sweep))))
log(f'wing4.val().isValid()={wing4.val().isValid()}')
show_object(wing4)

#pprint(vars(wing4))
import io
tolerance=0.001;
f = io.open(f'wing4-direct-{tolerance}.stl', 'w+')
cq.exporters.exportShape(wing4, cq.exporters.ExportTypes.STL, f, tolerance)
f.close()
