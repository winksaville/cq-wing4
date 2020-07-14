from naca5305 import naca5305
from scale import scaleListOfTuple
from fattenTe import fattenTe

import cadquery as cq # type: ignore

from typing import List, Sequence, Tuple

chord: float = 50 
h = 100

# Normalize, Scale, fattenTe
scaleFactor: float = 1/naca5305[0][0]
nNaca5305 = scaleListOfTuple(naca5305, scaleFactor)
sNaca5305: List[Tuple[float, float]] = scaleListOfTuple(nNaca5305, chord)
fNaca5305: List[Tuple[float, float]] = fattenTe(sNaca5305, 0.25, 10)

airfoil = (
    cq.Workplane("YZ")
    .spline(fNaca5305).close()
)

halfWing = (
    airfoil
    .extrude(h)
)
#show_object(halfWing)

# Shell the halfWing
halfWingShell = halfWing.shell(-0.1)
#show_object(halfWingShell)

