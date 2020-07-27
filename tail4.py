import cadquery as cq  # type: ignore

from ellipse import Ellipse
from naca0005 import naca0005
from rectcon import RectCon
from utils import show
from wing import Wing

chord = 15
span = 40
incidenceAngle = 0
dihedral = 45
sweep = 0

# Needs to be thick as it appears with the ribs it wants to
# print two layers. At 0.25, 0.26, 0.3 prusa-slicer only printed
# part of the LE and TE.
tk = 0.40

shortCut = False
wing = Wing.makeWing(
    airfoilSeq=naca0005,
    chord=chord,
    span=span,
    incidenceAngle=incidenceAngle,
    dihedral=dihedral,
    sweep=sweep,
    shellThickness=tk,
    ribCount=0,
    shortCut=shortCut,
    ctx=globals(),
)
show(wing, ctx=globals())

cabinLength: float = chord
cabinDiameter: float = 4.0
cabinYOffset: float = 0.0
cabinZOffset: float = 0  # -0.014
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
    f"tail4-tol_{tolerance}-ch_{chord}-span_{span}-ia_{incidenceAngle}-di_{dihedral}-tk_{tk}.stl", "w+"
)
cq.exporters.exportShape(wing4, cq.exporters.ExportTypes.STL, f, tolerance)
f.close()
