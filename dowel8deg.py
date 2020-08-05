import cadquery as cq  # type: ignore

from rectcon import RectCon
from utils import setCtx, show

setCtx(globals())

# Create dowel
c = RectCon(xLen=2.25, yLen=2.25, zLen=6, dowelAngle=8)
dowel = c.dowelHorz()
show(dowel)

import io

tolerance = 0.001
fname = f"dowel-tol_{tolerance:.4f}-x_{c.dowelBb.xlen:.4f}-y_{c.dowelBb.ylen:.4f}-z_{c.dowelBb.zlen:.4f}-a_{c.dowelAngle:.4f}.stl"
cq.exporters.export(beamHorz, fname, tolerance=tolerance)
