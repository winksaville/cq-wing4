import math
import sys
from typing import List, Sequence, Tuple

import cadquery as cq  # type: ignore

import airfoil as af
from fattenTe import fattenTe
from naca0005 import naca0005
from naca0020 import naca0020
from scale import scaleListOfTuple
from wing_utils import X, dbg, setCtx, show, translate_2d, updatePending, valid

setCtx(globals())


# The path that we'll sweep
path = cq.Workplane("XZ").moveTo(0, 30).radiusArc(endPoint=(30, 0), radius=30)
show(path, name="path")

# Sketch 1
#
# I get an Stanhdard_NullObject in the sweep command with naca0005.
# So I copied naca0005 to "t" below and commented out most of the
# points and it worked. I then slowly added them back and found that
# the problem is "fixed" if you comment out "Point TE 1 and Point TE 2".
# You can also fix the problem by making the circle in s2 >= 1.0 radius!
t: af.AirfoilSeq = af.AirfoilSeq(
    [
        (1.000000, 0.000525),
        (0.998459, 0.000615),  # Point TE 1
        (0.993844, 0.000884),
        (0.986185, 0.001326),
        (0.975528, 0.001934),
        (0.961940, 0.002699),
        (0.945503, 0.003607),
        (0.926320, 0.004645),
        (0.904508, 0.005798),
        (0.880203, 0.007048),
        (0.853553, 0.008378),
        (0.824724, 0.009772),
        (0.793893, 0.011210),
        (0.761249, 0.012676),
        (0.726995, 0.014151),
        (0.691342, 0.015615),
        (0.654508, 0.017049),
        (0.616723, 0.018432),
        (0.578217, 0.019743),
        (0.539230, 0.020959),
        (0.500000, 0.022058),
        (0.460770, 0.023017),
        (0.421783, 0.023812),
        (0.383277, 0.024421),
        (0.345492, 0.024823),
        (0.308658, 0.025000),
        (0.273005, 0.024937),
        (0.238751, 0.024622),
        (0.206107, 0.024048),
        (0.175276, 0.023212),
        (0.146447, 0.022118),
        (0.119797, 0.020772),
        (0.095492, 0.019187),
        (0.073680, 0.017377),
        (0.054497, 0.015361),
        (0.038060, 0.013158),
        (0.024472, 0.010789),
        (0.013815, 0.008272),
        (0.006156, 0.005626),
        (0.001541, 0.002865),
        (0.000000, 0.000000),
        (0.001541, -0.002865),
        (0.006156, -0.005626),
        (0.013815, -0.008272),
        (0.024472, -0.010789),
        (0.038060, -0.013158),
        (0.054497, -0.015361),
        (0.073680, -0.017377),
        (0.095492, -0.019187),
        (0.119797, -0.020772),
        (0.146447, -0.022118),
        (0.175276, -0.023212),
        (0.206107, -0.024048),
        (0.238751, -0.024622),
        (0.273005, -0.024937),
        (0.308658, -0.025000),
        (0.345492, -0.024823),
        (0.383277, -0.024421),
        (0.421783, -0.023812),
        (0.460770, -0.023017),
        (0.500000, -0.022058),
        (0.539230, -0.020959),
        (0.578217, -0.019743),
        (0.616723, -0.018432),
        (0.654508, -0.017049),
        (0.691342, -0.015615),
        (0.726995, -0.014151),
        (0.761249, -0.012676),
        (0.793893, -0.011210),
        (0.824724, -0.009772),
        (0.853553, -0.008378),
        (0.880203, -0.007048),
        (0.904508, -0.005798),
        (0.926320, -0.004645),
        (0.945503, -0.003607),
        (0.961940, -0.002699),
        (0.975528, -0.001934),
        (0.986185, -0.001326),
        (0.993844, -0.000884),
        (0.998459, -0.000615),  # Point TE 2
        (1.000000, -0.000525),
    ]
)
# s1 = cq.Workplane("YZ").polyline(translate_2d(scaleListOfTuple(t, 10.0), (-30, 30))).close()
s1 = (
    cq.Workplane("YZ")
    .polyline(translate_2d(scaleListOfTuple(naca0005, 100.0), (-30, 30)))
    .close()
)
# s1 = cq.Workplane("YZ").polyline(translate_2d(scaleListOfTuple(naca0020, 10.0), (-30, 30))).close()
# s1 = cq.Workplane("YZ").polyline(translate_2d(scaleListOfTuple([(1, 0), (0.4, 0.2), (0, 0), (0.4, -0.2)], 100.0), (-30, 30))).close()
show(s1, name="s1")


# Sketch 2

# Causes a Standard_Null error n sweep if circle
# radius is <= 0.5 and s1 is t, naca0005 or naca002
# s2 = cq.Workplane("XY").moveTo(30, 0).circle(0.5)

# s2 = cq.Workplane("XY").moveTo(30, 0).circle(10)
# s2 = cq.Workplane("XY").moveTo(30, 0).ellipse(5, 20)
s2 = (
    cq.Workplane("YX")
    .polyline(translate_2d(scaleListOfTuple(naca0020, 100.0), (-30, 30)))
    .close()
)
show(s2, name="s2")

# Add s2 to s1 so now s1 has 2 objects but there is only 1 pendingWire
c = s1.add(s2)
print(f"len(c.ctx.pendingWires)={len(c.ctx.pendingWires)}")

# This will result in 2 pendingWires
c = updatePending(c)

# This will result in 3 pendingWires and assert will fail
# c = c.toPending()

print(f"len(c.ctx.pendingWires)={len(c.ctx.pendingWires)}")
assert len(c.ctx.pendingWires) == 2
show(c, name="c")


# Sweep the results together
result = c.sweep(path, multisection=True)
show(result, name="result")
