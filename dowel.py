#!/usr/bin/env python3
import argparse
import math

import cadquery as cq  # type: ignore

from rectcon import RectCon
from utils import dbg, setCtx, show

setCtx(globals())

dfltDowelAngleDegrees: float = 0
dfltLinearPrecisionMm: float = 0.001
dfltAngularPrecisionDegrees: float = 1

parser = argparse.ArgumentParser()
parser.add_argument(
    "-a",
    "--dowelAngle",
    help=f"angle in degrees of a kinked dowel, default={dfltDowelAngleDegrees}",
    nargs="?",
    type=float,
    default=math.radians(dfltDowelAngleDegrees),
)
parser.add_argument(
    "-lp",
    "--linearPrecision",
    help=f"linear precision in milli-meters of stl file, default={dfltLinearPrecisionMm}",
    nargs="?",
    type=float,
    default=dfltLinearPrecisionMm,
)
parser.add_argument(
    "-ap",
    "--angularPrecision",
    help=f"angular precision in degrees of stl file, default={dfltAngularPrecisionDegrees}",
    nargs="?",
    type=float,
    default=math.radians(dfltAngularPrecisionDegrees),
)
args = parser.parse_args()

# Create dowel
c = RectCon(xLen=2.25, yLen=2.25, zLen=6, dowelAngle=args.dowelAngle)
dowel = c.dowelHorz()
show(dowel)

import io

linearPrecision: float = args.linearPrecision
angularPrecision: float = args.angularPrecision
fname = f"dowel-lp_{linearPrecision:.4f}-ap_{math.degrees(angularPrecision)}-x_{c.dowelBb.xlen:.4f}-y_{c.dowelBb.ylen:.4f}-z_{c.dowelBb.zlen:.4f}-a_{c.dowelAngle:.4f}.stl"
dbg(f"fname={fname}")
cq.exporters.export(
    dowel, fname, tolerance=linearPrecision, angularPrecision=angularPrecision
)
