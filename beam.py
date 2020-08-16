import sys

import cadquery as cq

from rectcon import RectCon
from wing_utils import dbg, setCtx, show

setCtx(globals())

c = RectCon(xLen=2.25, yLen=2.25, zLen=6)
# show(c.receiver)
# show(c.dowel)
# show(c.dowelHorz())

# beamLen = 30
# beam = cq.Workplane("XY").circle(beamDiameter / 2).extrude(beamLen)
# x = c.addReceiver(beam, ">Z")
# show(x)

# Create beam
beamLen = 30
beamDiameter = 4
beam = cq.Workplane("XY").circle(beamDiameter / 2).extrude(beamLen)
beamVert = beam.cut(
    c.receiver.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, beamLen))
).cut(c.receiver)
# show(beamVert)
beamHorz = beamVert.rotate((0, 0, 0), (1, 0, 0), 90).translate((0, 0, beamDiameter / 2))
show(beamHorz)

import io

tolerance = 0.001
fname = f"beam-tol_{tolerance:.4f}-dia_{beamDiameter:.4f}-len_{beamLen}-recv-x_{c.receiverBb.xlen:.4f}-y_{c.receiverBb.ylen:.4f}-z_{c.receiverBb.zlen:.4f}.stl"
cq.exporters.export(beamHorz, fname, tolerance=tolerance)
