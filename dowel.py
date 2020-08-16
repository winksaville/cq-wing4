#!/usr/bin/env python3
import argparse
import math
import sys

import cadquery as cq

from rectcon import RectCon
from wing_utils import dbg, setCtx, show

setCtx(globals())

cq_editor_cmdline: str = "-a 20"

dfltReceiver_xLen: float = 2.25
dfltReceiver_yLen: float = 2.25
dfltReceiver_zLen: float = 6
dfltDowelAngleDegrees: float = 0
dfltDowelClearence: float = 0.05
dfltLinearTolerance: float = 0.001
dfltAngularToleranceDegrees: float = 0.1


receiver_xLen: float
receiver_yLen: float
receiver_zLen: float
dowelAngleDegrees: float
dowelClearence: float
linearTolerance: float
angularToleranceDegrees: float

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
    "-x",
    "--receiver_xLen",
    help=f"X length in mm, default={dfltReceiver_xLen}",
    nargs="?",
    type=float,
    default=dfltReceiver_xLen,
)
parser.add_argument(
    "-y",
    "--receiver_yLen",
    help=f"Y length in mm, default={dfltReceiver_yLen}",
    nargs="?",
    type=float,
    default=dfltReceiver_yLen,
)
parser.add_argument(
    "-z",
    "--receiver_zLen",
    help=f"Z length in mm, default={dfltReceiver_zLen}",
    nargs="?",
    type=float,
    default=dfltReceiver_zLen,
)
parser.add_argument(
    "-c",
    "--dowelClearence",
    help=f"Clearence in mm per side, 2 * dowelClearence subtracted from x and y, default={dfltDowelClearence}",
    nargs="?",
    type=float,
    default=dfltDowelClearence,
)
parser.add_argument(
    "-lt",
    "--linearTolerance",
    help=f"linear precision in mm of stl file, default={dfltLinearTolerance}",
    nargs="?",
    type=float,
    default=dfltLinearTolerance,
)
parser.add_argument(
    "-at",
    "--angularTolerance",
    help=f"angular precision in degrees of stl file, default={dfltAngularToleranceDegrees}",
    nargs="?",
    type=float,
    default=dfltAngularToleranceDegrees,
)

if "cq_editor" in sys.modules:
    args = parser.parse_args(cq_editor_cmdline.split())
else:
    args = parser.parse_args()

receiver_xLen = args.receiver_xLen
receiver_yLen = args.receiver_yLen
receiver_zLen = args.receiver_zLen
dowelAngleDegrees = args.dowelAngle
dowelClearence = args.dowelClearence
linearTolerance = args.linearTolerance
angularToleranceDegrees = args.angularTolerance

dbg(f"x={receiver_xLen}, y={receiver_yLen}, z={receiver_zLen}, a={dowelAngleDegrees}")

# Create dowel
c = RectCon(
    xLen=receiver_xLen,
    yLen=receiver_yLen,
    zLen=receiver_zLen,
    dowelAngle=dowelAngleDegrees,
)
dowel = c.dowelHorz()
show(dowel)

import io

fname = f"dowel-x_{c.dowel_xLen:.4f}-y_{c.dowel_yLen:.4f}-z_{c.dowel_zLen:.4f}-a_{c.dowelAngle:.4f}-lt_{linearTolerance:.4f}-at_{angularToleranceDegrees:.4f}.stl"
dbg(f"fname={fname}")
cq.exporters.export(
    dowel,
    fname,
    tolerance=linearTolerance,
    angularTolerance=math.radians(angularToleranceDegrees),
)
