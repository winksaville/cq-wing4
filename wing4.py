import cadquery as cq  # type: ignore

from ellipse import Ellipse
from naca5305 import naca5305
from utils import show
from wing import Wing

chord = 50
span = 200
incidenceAngle = 2
dihedral = 5
sweep = 0
tk = 0.25
wing = Wing.makeWing(
    airfoilSeq=naca5305,
    chord=chord,
    span=span,
    incidenceAngle=incidenceAngle,
    dihederal=dihedral,
    sweep=sweep,
    shellThickness=tk,
    ctx=globals(),
)
show(wing, ctx=globals())

cabinProfile = Ellipse(xLen=6, yLen=10)
cabin = (
    cq.Workplane("XZ")
    .ellipse(cabinProfile.xAxis(), cabinProfile.yAxis())
    .extrude(chord)
    .rotate((0, 0, 0), (1, 0, 0), -90)
)
show(cabin, ctx=globals())

# c = RectCon()
# # show(c.male, ctx=globals())
#
# bodyEllipse2d = Ellipse(xLen=8, yLen=12)
#
# bodyLen = 30
# body = (
#     cq.Workplane("XY")
#     .ellipse(bodyEllipse2d.xAxis(), bodyEllipse2d.yAxis())
#     .extrude(bodyLen)
# )
# body1 = body.cut(
#     c.female.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, bodyLen))
# ).cut(c.female)
# # show(body1, ctx=globals())
#
# body2 = body1.translate((20, 0, 0))
# # show(body2, ctx=globals())
#
# stick1 = (
#     c.male.rotate((0, 0, 0), (1, 0, 0), 180)
#     .union(c.male)
#     .translate((0, 0, c.maleBb.zlen))
# )
# stick1 = stick1.translate((40, 0, 0))
# # show(stick1, ctx=globals())
# stick2 = stick1.translate((20, 0, 0))
# # show(stick2, ctx=globals())
#
# bodies = (
#     body1.add(body2)
#     .combine()
#     .rotate((0, 0, 0), (1, 0, 0), 90)
#     .translate((0, 0, bodyEllipse2d.yLen / 2))
# )
# sticks = (
#     stick1.add(stick2)
#     .combine()
#     .rotate((0, 0, 0), (1, 0, 0), 90)
#     .translate((0, 0, c.maleBb.ylen / 2))
# )
# result = bodies.add(sticks).combine()
# show(result)

import io

tolerance = 0.001
f = io.open(f"wing4-tol_{tolerance}-tk_{tk}.stl", "w+")
cq.exporters.exportShape(wing, cq.exporters.ExportTypes.STL, f, tolerance)
f.close()
