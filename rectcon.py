import math
from copy import copy, deepcopy
from dataclasses import dataclass
from typing import List, Sequence, Tuple

import cadquery as cq  # type: ignore

from utils import dbg, show


class RectCon:
    """
    An Rectangular Connector
    """

    female: cq.Workplane
    femaleBb: cq.Workplane

    male: cq.Workplane
    maleBb: cq.Workplane

    def __init__(
        self,
        zLen: float = 6,
        xLen: float = 2.25,
        yLen: float = 2.25,
        fillets=0.250,
        ctx: object = None,
    ) -> None:
        dbg(f"RectCon.init: xLen={xLen} yLen={yLen} zLen={zLen}")

        r = (
            cq.Workplane("XY")
            .rect(xLen, yLen)
            .extrude(zLen)
            .edges(">Z")
            .fillet(fillets)
        )
        rBb = r.val().BoundingBox()
        dbg(f"rBb: xlen={rBb.xlen} ylen={rBb.ylen} zlen={rBb.zlen}")
        # show(e, ctx=globals())

        self.male = r
        self.maleBb = self.male.val().BoundingBox()
        dbg(
            f"maleBb: xlen={self.maleBb.xlen} ylen={self.maleBb.ylen} zlen={self.maleBb.zlen}"
        )

        self.female = r
        self.femaleBb = self.female.val().BoundingBox()
        dbg(
            f"femaleBb: xlen={self.femaleBb.xlen} ylen={self.femaleBb.ylen} zlen={self.maleBb.zlen}"
        )


if __name__ == "__main__" or "show_object" in globals():

    c = RectCon(xLen=2.25, yLen=2.25, zLen=6)
    # show(c.male, ctx=globals())

    body2dRadius = 2

    bodyLen = 30
    body = cq.Workplane("XY").circle(body2dRadius).extrude(bodyLen)
    body1 = body.cut(
        c.female.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, bodyLen))
    ).cut(c.female)
    # show(body1, ctx=globals())

    body2 = body1.translate((20, 0, 0))
    # show(body2, ctx=globals())

    # Rotate body1 horizitonal leave body2 vertical
    body1 = body1.rotate((0, 0, 0), (1, 0, 0), 90).translate((0, 0, body2dRadius))

    stick1 = (
        c.male.rotate((0, 0, 0), (1, 0, 0), 180)
        .union(c.male)
        .translate((0, 0, c.maleBb.zlen))
    )
    stick1 = stick1.translate((40, 0, 0))
    # show(stick1, ctx=globals())
    stick2 = stick1.translate((20, 0, 0))
    # show(stick2, ctx=globals())

    bodies = body1.add(body2).combine()
    sticks = (
        stick1.add(stick2)
        .combine()
        .rotate((0, 0, 0), (1, 0, 0), 90)
        .translate((0, 0, c.maleBb.ylen / 2))
    )
    result = bodies.add(sticks).combine()
    show(result)

    import io

    tolerance = 0.001
    f = io.open(
        f"rectcon-tol_{tolerance}-rad_{body2dRadius}-x_{c.maleBb.xlen}-y_{c.maleBb.ylen}.stl",
        "w+",
    )
    cq.exporters.exportShape(result, cq.exporters.ExportTypes.STL, f, tolerance)
    f.close()
