from naca5305 import naca5305
from scale import scaleListOfTuple
from fattenTe import fattenTe

import cadquery as cq # type: ignore

chord: float = 50 
h = 100

# Normalize, Scale, fattenTe
scaleFactor = 1/naca5305[0][0]
nNaca5305 = scaleListOfTuple(naca5305, scaleFactor)
sNaca5305 = scaleListOfTuple(nNaca5305, chord)
#fNaca5305 = fattenTe(sNaca5305, 0.25, 10)
fNaca5305 = sNaca5305

# Create the 2D airfoil then extrude
airfoil = cq.Workplane("YZ").spline(fNaca5305).close()
halfWing = airfoil.extrude(h)

# Shell the halfWing
halfWingShell = halfWing.shell(0.1)
show_object(halfWingShell)
#show_object(halfWing)
#show_object(airfoil)

