import math
import sys
from typing import List, Sequence, Tuple, cast

import cadquery as cq

import airfoil as af
import rectcon as rc
from fattenTe import fattenTe
from naca0020 import naca0020
from scale import scaleListOfTupleByTuple
from wing_utils import dbg, setCtx, show, split_2d

setCtx(globals())

# Connector for stub at the trailing edge of the ballast bulb
c_xLen: float = 2.25
c_yLen: float = 2.25
c_zLen: float = 6

# Dimensions for ballast bulb
length: float = 15
wallThickness: float = 0.5
stubMinLength: float = c_zLen + 0.5
stubProtuding: float = 1
stubDiameter: float = 4
stubThickness: float = 4

# We scale Y to be twice as big as X to create a naca0040 from naca0020
scaleX: float = length
scaleY: float = length * 2

# Scale a naca0020
f = cast(List[Tuple[float, float]], scaleListOfTupleByTuple(naca0020, (scaleX, scaleY)))
# dbg(f"f={f}")

# Split f in half
hf = split_2d(linePt1=(0, 0), linePt2=(1, 0), lst=f)
wp_hf = cq.Workplane("XY").polyline(hf).close()
# show(wp_hf, "wp_hf")
solid = wp_hf.revolve(axisStart=(0, 0), axisEnd=(1, 0))
# show(solid, "solid")

# TODO: Create wing_utils.offset_2d so we don't have to
# create a workplane to do this. Or better yet teach
# cq.Workplane to properly handle the "*_2d" operations
# we have in wing_utils.
s0 = cq.Workplane("XY").polyline(f).close()
s1 = s0.offset2D(-wallThickness, "intersection")
s1v = [(v.X, v.Y) for v in cast(cq.Shape, s1.val()).Vertices()]
s1vh = split_2d((0, 0), (1, 0), s1v)

# Create workplane  and revolve to make cutter
wp_s1vh = cq.Workplane("XY").polyline(s1vh).close()
# show(wp_s1vh, "wp_s1vh")
cutter = wp_s1vh.revolve(axisStart=(0, 0), axisEnd=(1, 0))
# show(cutter, "cutter")

# Intersection of solid and cutter is the ballast
ballast = solid.cut(cutter)
# show(ballast, "ballast")

# Find what X position where Y is > 0.5 * stubThickness,
# ASSUMPTION: Trailing Edge is at hf[0].
stubX: float
stubY: float
for stubX, stubY in hf:
    if stubY > (0.5 * stubThickness):
        break
stubLength: float = max(stubMinLength, (length - stubX) + stubProtuding)
# dbg(f"stubX={stubX}")
# dbg(f"stubY={stubY}")
# dbg(f"stubLength={stubLength}")

# Create stub
stub = (
    cq.Workplane("YZ", origin=(stubX, 0, 0))
    .circle(stubDiameter / 2)
    .extrude(stubLength)
)
# show(stub, "stub")

ballastWithStub = ballast.union(stub)
# show(ballastWithStub, "ballastWithStub")

receiver = rc.RectCon(xLen=c_xLen, yLen=c_yLen, zLen=c_zLen).receiver
# show(receiver, "receiver")

result = ballastWithStub.cut(
    receiver.rotate((0, 0, 0), (0, 1, 0), -90).translate((stubX + stubLength, 0, 0))
)
show(result, "result")
