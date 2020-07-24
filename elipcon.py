import math
from copy import copy, deepcopy
from dataclasses import dataclass
from typing import List, Sequence, Tuple

import cadquery as cq  # type: ignore

from utils import dbg, show


@dataclass
class Ellipse:
    xLen: float
    yLen: float

    def xAxis(self):
        return self.xLen / 2

    def yAxis(self):
        return self.yLen / 2


class EllipseCon:
    """
    An Ellipitical Connector
    """

    femaleCutter: cq.Shape
    male: cq.Shape

    def __init__(self, elip: Ellipse, height: float, ctx: object = None,) -> None:
        dbg(f"Ellipse.make: elip={elip} height={height}")

        fillets = 0.125

        base_xAxis = elip.xAxis()
        base_yAxis = elip.yAxis()

        waistWidthFactor = 0.5
        waist_xAxis = elip.xAxis() * waistWidthFactor
        waist_yAxis = elip.yAxis() * waistWidthFactor

        shoulderWidthFactor = waistWidthFactor * 1.2
        shoulderWidthX = elip.xLen * shoulderWidthFactor
        shoulderWidthY = elip.yLen * shoulderWidthFactor
        shoulder_xAxis = elip.xAxis() * shoulderWidthFactor
        shoulder_yAxis = elip.yAxis() * shoulderWidthFactor

        tipWidthFactor = waistWidthFactor
        tipWidthX = elip.xLen * tipWidthFactor
        tipWidthY = elip.yLen * tipWidthFactor
        tip_xAxis = elip.xAxis() * tipWidthFactor
        tip_yAxis = elip.yAxis() * tipWidthFactor

        reliefWidthX = shoulderWidthX - tipWidthX  # * 1.5
        reliefWidthY = shoulderWidthY - tipWidthY  # * 1.5
        reliefLen = height * 0.75
        reliefHeight = height - reliefLen

        waistHeight = height / 2
        waistToShoulder = waistHeight / 2
        shoulderToTip = height - waistHeight - waistToShoulder

        e = (
            cq.Workplane("XY")
            .ellipse(base_xAxis, base_yAxis)
            .workplane(offset=waistHeight)
            .ellipse(waist_xAxis, waist_yAxis)
            .loft(combine=True)
            .faces(">Z")
            .ellipse(waist_xAxis, waist_yAxis)
            .workplane(offset=waistToShoulder)
            .ellipse(shoulder_xAxis, shoulder_yAxis)
            .loft(combine=True)
            .faces(">Z")
            .ellipse(shoulder_xAxis, shoulder_yAxis)
            .workplane(offset=shoulderToTip)
            .ellipse(tip_xAxis, tip_yAxis)
            .loft(combine=True)
            .edges(">Z")
            .fillet(fillets)
        )
        eBb = e.val().BoundingBox()
        dbg(f"eBb: xlen={eBb.xlen} ylen={eBb.ylen} zlen={eBb.zlen}")
        # show(e, ctx=globals())

        reliefOther = max(elip.xLen, elip.yLen)
        xRelief = (
            cq.Workplane("XY", origin=(0, 0, reliefHeight))
            .rect(reliefOther, reliefWidthY)
            .extrude(height)
            .edges("<Z")
            .fillet(fillets)
        )
        # show(xRelief, ctx=globals())

        yRelief = (
            cq.Workplane("XY", origin=(0, 0, reliefHeight))
            .rect(reliefWidthX, reliefOther)
            .extrude(height)
            .edges("<Z")
            .fillet(fillets)
        )
        # show(yRelief, ctx=globals())

        # Cut out the reliefs
        self.male = e.cut(yRelief).cut(xRelief)
        # self.male = e.cut(xRelief).cut(yRelief) # BAD, why?
        # show(self.male, ctx=globals())

        maleBb = self.male.val().BoundingBox()
        dbg(f"maleBb: xlen={maleBb.xlen} ylen={maleBb.ylen} zlen={maleBb.zlen}")

        self.female = e
        femaleBb = self.female.val().BoundingBox()
        dbg(f"femaleBb: xlen={femaleBb.xlen} ylen={femaleBb.ylen} zlen={maleBb.zlen}")


if __name__ == "__main__" or "show_object" in globals():
    c = EllipseCon(Ellipse(xLen=6, yLen=10), height=10)
    # show(c.male, ctx=globals())

    bodyEllipse2d = Ellipse(xLen=8, yLen=12)

    bodyLen = 20
    body = (
        cq.Workplane("XY")
        .ellipse(bodyEllipse2d.xAxis(), bodyEllipse2d.yAxis())
        .extrude(bodyLen)
    )
    body = c.male.translate((0, 0, bodyLen)).union(body)
    body1 = body.cut(c.female)
    # show(body1, ctx=globals())

    body2 = copy(body1).translate((20, 0, 0))
    # show(body2, ctx=globals())

    result = (
        body1.add(body2)
        .combine()
        .rotate((0, 0, 0), (1, 0, 0), 90)
        .translate((0, 0, bodyEllipse2d.yLen / 2))
    )
    show(result)

    import io

    tolerance = 0.001
    f = io.open(f"elipcon-tol_{tolerance}.stl", "w+")
    cq.exporters.exportShape(result, cq.exporters.ExportTypes.STL, f, tolerance)
    f.close()
