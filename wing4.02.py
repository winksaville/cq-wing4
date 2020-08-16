import cadquery as cq

from ellipse import Ellipse
from naca5305 import naca5305
from rectcon import RectCon
from wing import Wing
from wing_utils import dbg, setCtx, show

setCtx(globals())

chord = 50
span = 200
incidenceAngle = 2
dihedral = 5
sweep = 0
tk = 0.26  # 0.25 prusa-slicer didn't print 1/4 of the wing
shortCut = False
wing = Wing.makeWing(
    airfoilSeq=naca5305,
    chord=chord,
    span=span,
    incidenceAngle=incidenceAngle,
    dihedral=dihedral,
    sweep=sweep,
    shellThickness=tk,
    shortCut=shortCut,
)
# Flip the wing so it LE is on the plate. I did this because
# the last print the cabin warpped by 8degrees.
wing = wing.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, chord))
# show(wing, name="wing")

# TODO: We fudge cabinLength so we are slightly past the trailing edge.
# If we don't the trailing edge sticks ever so slightly past the cabin, why?
cabinLength: float = chord * 1.001
cabinDiameter: float = 4.0
cabinYOffset: float = -1.0
cabinZOffset: float = 0
cabin = (
    cq.Workplane("XZ")
    .circle(cabinDiameter / 2)
    .extrude(cabinLength)
    .rotate((0, 0, 0), (1, 0, 0), -90)
    .translate((0, cabinYOffset, cabinZOffset))
)
# show(cabin, name="cabin")

wingCabin = wing.union(cabin)
# show(wingCabin, name="wingCabin")

c = RectCon(xLen=2.25, yLen=2.25, zLen=6)
# show(c.male, name="c.male")

wing4 = wingCabin.cut(
    c.receiver.rotate((0, 0, 0), (1, 0, 0), 180).translate(
        (0, cabinYOffset, cabinLength)
    )
).cut(c.receiver.translate((0, cabinYOffset, cabinZOffset)))
show(wing4, name="wing4")

import io

tolerance = 0.001
f = io.open(
    f"wing4.02-LE-down-tol_{tolerance}-ch_{chord}-span_{span}-di_{dihedral}-tk_{tk}.stl",
    "w+",
)
cq.exporters.exportShape(wing4, cq.exporters.ExportTypes.STL, f, tolerance)
f.close()
