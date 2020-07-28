import math
import typing
from copy import copy, deepcopy
from dataclasses import dataclass
from typing import Tuple

import cadquery as cq  # type: ignore

from utils import dbg, show


class RectCon:
    """
    A Rectangular Connector composed of a receiver and a dowel.
    The orientation for both is sitting vertically on the XY plane
    centered at the origin.
    """

    receiver: cq.Workplane
    receiverBb: cq.Workplane

    dowel: cq.Workplane
    dowelBb: cq.Workplane

    def __init__(
        self,
        zLen: float = 6,
        xLen: float = 2.25,
        yLen: float = 2.25,
        dowelShrinkage: float = 0.05,
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

        self.receiver = r
        self.receiverBb = self.receiver.val().BoundingBox()
        dbg(
            f"receiverBb: xlen={self.receiverBb.xlen} ylen={self.receiverBb.ylen} zlen={self.receiverBb.zlen}"
        )
        # show(self.receiver, ctx=globals())

        halfD = (
            cq.Workplane("XY")
            .rect(xLen * (1 - dowelShrinkage), yLen * (1 - dowelShrinkage))
            .extrude(zLen)
            .edges(">Z")
            .fillet(fillets)
        )

        d = (
            halfD.rotate((0, 0, 0), (1, 0, 0), 180).union(halfD)
            # .rotate((0, 0, 0), (1, 0, 0), 90)
            .translate((0, 0, zLen))
        )
        self.dowel = d
        self.dowelBb = self.dowel.val().BoundingBox()
        dbg(
            f"dowelBb: xlen={self.dowelBb.xlen} ylen={self.dowelBb.ylen} zlen={self.dowelBb.zlen}"
        )
        # show(self.dowel, ctx=globals())

    def dowelHorz(self) -> cq.Workplane:
        """
        Return dowel so its Horzitional laying on the XY plane
        centered on the Z axis.
        """
        return self.dowel.rotate((0, 0, 0), (1, 0, 0), 90).translate(
            (0, self.dowelBb.zlen / 2, self.dowelBb.ylen / 2)
        )

    def addReceiver(
        self,
        shape: cq.Workplane,
        face: str,
        location: Tuple[float, float, float] = (0, 0, 0),
    ) -> cq.Workplane:
        """
        Add a receiver to the face of the shape passed.
        """

        show(shape, ctx=globals())
        f = shape.faces(face)
        dbg(f"f={f}")
        show(f, ctx=globals())
        r = self.receiver
        show(r, ctx=globals())
        # f.cut(self.receiver.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, bodyLen))
        # cq.SelectbodyLen = 30
        # body = cq.Workplane("XY").circle(bodyDiameter / :2).extrude(bodyLen)
        # body1 = body.cut(
        #    c.receiver.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, bodyLen))
        # ).cut(c.receiver)
        # show(body1, ctx=globals())
        return shape


if __name__ == "__main__" or "show_object" in globals():

    c = RectCon(xLen=2.25, yLen=2.25, zLen=6)
    # show(c.receiver, ctx=globals())
    # show(c.dowel, ctx=globals())
    # show(c.dowelHorz(), ctx=globals())

    # bodyLen = 30
    # body = cq.Workplane("XY").circle(bodyDiameter / 2).extrude(bodyLen)
    # x = c.addReceiver(body, ">Z")
    # show(x, ctx=globals())

    # Create poles
    bodyLen = 30
    bodyDiameter = 4
    body = cq.Workplane("XY").circle(bodyDiameter / 2).extrude(bodyLen)
    bodyVert = body.cut(
        c.receiver.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, bodyLen))
    ).cut(c.receiver)
    # show(bodyVert, ctx=globals())
    bodyHorz = bodyVert.rotate((0, 0, 0), (1, 0, 0), 90).translate(
        (20, 0, bodyDiameter / 2)
    )
    # show(bodyHorz, ctx=globals())

    # Create dowels
    dowel1 = c.dowelHorz().translate((40, 0, 0))
    # show(dowel1, ctx=globals())
    dowel2 = c.dowelHorz().translate((60, 0, 0))
    # show(dowel2, ctx=globals())

    result = bodyHorz.add(bodyVert).add(dowel1).add(dowel2).combine()
    show(result, ctx=globals())

    import io

    tolerance = 0.001
    f = io.open(
        f"rectcon-tol_{tolerance:.4f}-dia_{bodyDiameter:.4f}-x_{c.dowelBb.xlen:.4f}-y_{c.dowelBb.ylen:.4f}.stl",
        "w+",
    )
    cq.exporters.exportShape(result, cq.exporters.ExportTypes.STL, f, tolerance)
    f.close()
