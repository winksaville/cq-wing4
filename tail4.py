import cadquery as cq  # type: ignore

from ellipse import Ellipse
from naca0005 import naca0005
from rectcon import RectCon
from utils import show
from wing import Wing

chord = 15
span = 40
tk = 0.40

horzStabilizer = cq.Workplane("XY").box(chord, span, tk).translate((0, 0, tk / 2))
# show(horzStabilizer, ctx=globals())

vertStabilizer = (
    cq.Workplane("XY")
    .box(chord, span / 2, tk)
    .rotate((0, 0, 0), (1, 0, 0), 90)
    .translate((0, 0, span / 4))
)
# show(vertStabilizer, ctx=globals())

stabilizer = horzStabilizer.union(vertStabilizer)
# show(stabilizer, ctx=globals())

boomLength: float = chord
boomDiameter: float = 4.0
boomXOffset: float = chord / 2
boomYOffset: float = 0
boomZOffset: float = +boomDiameter / 2
boom = (
    cq.Workplane("XZ")
    .circle(boomDiameter / 2)
    .extrude(chord)
    .rotate((0, 0, 0), (0, 0, 1), -90)
    .translate((boomXOffset, boomYOffset, boomZOffset))
)
# show(boom, ctx=globals())

tail = stabilizer.union(boom)

c = RectCon(xLen=2.25, yLen=2.25, zLen=6)
xCut = c.male.rotate((0, 0, 0), (0, 1, 0), 90).translate(
    (-chord / 2, 0, boomDiameter / 2)
)
yCut = c.male.rotate((0, 0, 0), (0, 1, 0), 270).translate(
    (chord / 2, 0, boomDiameter / 2)
)
# show(c.male, ctx=globals())
# show(xCut, ctx=globals())
# show(yCut, ctx=globals())

tail4 = tail.cut(xCut).cut(yCut)
show(tail4, ctx=globals())

import io

tolerance = 0.001
f = io.open(f"tail4-tol_{tolerance}-ch_{chord}-span_{span}-tk_{tk}.stl", "w+")
cq.exporters.exportShape(tail4, cq.exporters.ExportTypes.STL, f, tolerance)
f.close()
