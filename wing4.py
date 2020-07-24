import cadquery as cq  # type: ignore

import utils as ut
import wing as w
from naca5305 import naca5305

tk = 0.25
wing = w.Wing.makeWing(airfoilSeq=naca5305, shellThickness=tk, ctx=globals())
ut.show(wing, ctx=globals())

import io

tolerance=0.001;
f = io.open(f'wing4-tol_{tolerance}-tk_{tk}.stl', 'w+')
cq.exporters.exportShape(wing, cq.exporters.ExportTypes.STL, f, tolerance)
f.close()
