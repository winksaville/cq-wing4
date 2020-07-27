import cadquery as cq  # type: ignore

from ellipse import Ellipse
from naca5305 import naca5305
from rectcon import RectCon
from utils import show
from wing import Wing

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
    ctx=globals(),
)
# show(wing, ctx=globals())

# TODO: We fudge cabin Z position so it aligns with trailing edge, why?
cabinLength: float = chord
cabinDiameter: float = 4.0
cabinYOffset: float = 1.0
cabinZOffset: float = -0.014
cabin = (
    cq.Workplane("XZ")
    .circle(cabinDiameter / 2)
    .extrude(chord)
    .rotate((0, 0, 0), (1, 0, 0), -90)
    .translate((0, cabinYOffset, cabinZOffset))
)
# show(cabin, ctx=globals())

wingCabin = wing.union(cabin)
# show(wingCabin, ctx=globals())

c = RectCon(xLen=2.25, yLen=2.25, zLen=6)
# show(c.male, ctx=globals())

wing4 = wingCabin.cut(
    c.female.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, cabinYOffset, chord))
).cut(c.female.translate((0, cabinYOffset, cabinZOffset)))
show(wing4, ctx=globals())

import io

tolerance = 0.001
f = io.open(
    f"wing4-tol_{tolerance}-ch_{chord}-span_{span}-di_{dihedral}-tk_{tk}.stl", "w+"
)
cq.exporters.exportShape(wing4, cq.exporters.ExportTypes.STL, f, tolerance)
f.close()
