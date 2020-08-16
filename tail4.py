import cadquery as cq

from ellipse import Ellipse
from naca0005 import naca0005
from rectcon import RectCon
from wing import Wing
from wing_utils import show

chord = 20
span = 80
tk = 0.40

horzStabilizer = cq.Workplane("XY").box(chord, span, tk).translate((0, 0, tk / 2))
# show(horzStabilizer)

vertStabilizer = (
    cq.Workplane("XY")
    .box(chord, span / 2, tk)
    .rotate((0, 0, 0), (1, 0, 0), 90)
    .translate((0, 0, span / 4))
)
# show(vertStabilizer)

stabilizer = horzStabilizer.union(vertStabilizer)
# show(stabilizer)

boomLength: float = chord
boomDiameter: float = 4.0
boomXOffset: float = chord / 2
boomYOffset: float = 0
boomZOffset: float = +boomDiameter / 2
boom = (
    cq.Workplane("XZ")
    .circle(boomDiameter / 2)
    .workplane(offset=chord)
    .circle(boomDiameter / 6)
    .loft(combine=True)
    .rotate((0, 0, 0), (0, 0, 1), -90)
    .translate((boomXOffset, boomYOffset, boomZOffset))
)
# show(boom)

tail = stabilizer.union(boom)

c = RectCon(xLen=2.25, yLen=2.25, zLen=6)
cut = c.receiver.rotate((0, 0, 0), (0, 1, 0), 270).translate(
    (chord / 2, 0, boomDiameter / 2)
)
# show(c.male)
# show(cut)

tail4 = tail.cut(cut)
show(tail4)

import io

tolerance = 0.001
f = io.open(f"tail4-tol_{tolerance}-ch_{chord}-span_{span}-tk_{tk}.stl", "w+")
cq.exporters.exportShape(tail4, cq.exporters.ExportTypes.STL, f, tolerance)
f.close()
