import typing
from dataclasses import dataclass
from math import cos, degrees, radians, sin
from typing import Tuple

import cadquery as cq  # type: ignore

from utils import X, Y, Z, dbg, show


class RectCon:
    """
    A Rectangular Connector composed of a receiver and a dowel.
    The orientation for both is sitting vertically on the XY plane
    centered at the origin.

    dowelAngle max=70 min=0

    TODO: dowelAngles <0 and >70 degrees fail, why?
    """

    receiver: cq.Workplane
    receiverBb: cq.Workplane

    dowel: cq.Workplane
    dowelBb: cq.Workplane
    dowelAngle: float
    dowel_xLen: float
    dowel_yLen: float

    def __init__(
        self,
        zLen: float = 6,
        xLen: float = 2.25,
        yLen: float = 2.25,
        dowelAngle: float = 0.0,  # Maximum is 70deg(?) negs not supported(?)
        dowelShrinkage: float = 0.05,
        fillets: float = 0.250,
        ctx: object = None,
    ) -> None:
        dbg(f"RectCon.init: xLen={xLen} yLen={yLen} zLen={zLen}")

        # Create the receiver
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
            f"receiverBb: xlen={self.receiverBb.xlen} ylen={self.receiverBb.ylen} zlen={self.receiverBb.zlen} a={dowelAngle}"
        )
        # show(self.receiver)

        # Compute basic dowel dimensions
        dowel_xLen = xLen * (1 - dowelShrinkage)
        dowel_yLen = yLen * (1 - dowelShrinkage)

        # Bottom portion of Dowel
        bottomD = (
            cq.Workplane("XY")
            .rect(dowel_xLen, dowel_yLen)
            .extrude(zLen)
            .faces("<Z")
            .fillet(fillets)
        )
        # show(bottomD)

        if dowelAngle != 0:
            # TODO: Figure out why 0 doesn't work for this path

            # Wedge dimensions
            halfA = radians(dowelAngle / 2)
            chord: float = dowel_yLen * sin(halfA) * 2
            sag: float = dowel_yLen * (1 - cos(halfA))
            g: float = radians(90) - halfA
            epX: float = -sin(g) * chord
            epY: float = cos(g) * chord
            ep: Tuple[float, float] = (epX, epY)
            dbg(
                f"halfA={degrees(halfA)} chord={chord} sag={sag}, g={degrees(g)} ep={ep}"
            )

            # Workplane for creating the wedge
            wedgeWp = (
                bottomD.faces("<Y")
                .vertices("<X and >Z")
                .workplane()
                .transformed(rotate=cq.Vector(0, +90, 0))
            )
            # show(wedgeWp.circle(0.2))
            # show(wedgeWp.moveTo(1, 1).circle(0.2))

            # Create the wedge
            wedge = (
                wedgeWp.sagittaArc(ep, sag)
                .moveTo(ep[X], ep[Y])
                .lineTo(0, dowel_yLen)
                .close()
                .extrude(dowel_yLen)
            )
            # show(wedge)

            bottomAndWedge = bottomD.union(wedge)
            # show(bottomAndWedge)

            # Workplane for top portion of Dowel
            topWp = (
                bottomAndWedge.faces(">Y")
                .vertices(">Z and <X")
                .workplane()
                .transformed(rotate=cq.Vector(-dowelAngle, 0, 0))
                .moveTo(dowel_xLen / 2, -dowel_yLen / 2)
            )
            # show(topWp.circle(0.2))
        else:
            bottomAndWedge = bottomD
            topWp = bottomAndWedge.faces(">Z").workplane()
        # show(bottomAndWedge)

        # Top portion of dowel
        topD = (
            topWp.rect(dowel_xLen, dowel_yLen).extrude(zLen).faces(">Z").fillet(fillets)
        )
        # show(topD)

        # The competed dowel
        completeD = bottomAndWedge.union(topD)
        # show(completeD)

        self.dowel = completeD
        self.dowelBb = self.dowel.val().BoundingBox()
        self.dowel_xLen = dowel_xLen
        self.dowel_yLen = dowel_yLen
        self.dowelAngle = dowelAngle
        dbg(
            f"dowelBb: xlen={self.dowelBb.xlen} ylen={self.dowelBb.ylen} zlen={self.dowelBb.zlen} a={self.dowelAngle}"
        )
        # show(self.dowel)

    def dowelHorz(self) -> cq.Workplane:
        """
        Return dowel so its Horzitional laying on the XY plane
        centered on the Z axis.
        """
        return (
            self.dowel.rotate((0, 0, 0), (1, 0, 0), 90)
            .rotate((0, 0, 0), (0, 1, 0), 90)
            .translate((0, 0, self.dowel_yLen / 2))
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

        show(shape)
        f = shape.faces(face)
        dbg(f"f={f}")
        show(f)
        r = self.receiver
        show(r)
        # f.cut(self.receiver.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, bodyLen))
        # cq.SelectbodyLen = 30
        # body = cq.Workplane("XY").circle(bodyDiameter / :2).extrude(bodyLen)
        # body1 = body.cut(
        #    c.receiver.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, bodyLen))
        # ).cut(c.receiver)
        # show(body1)
        return shape


if __name__ == "__main__" or "show_object" in globals():

    c = RectCon(xLen=2.25, yLen=2.25, zLen=6, dowelAngle=8.0)
    # show(c.receiver)
    # show(c.dowel)
    # show(c.dowelHorz())

    # Create beam
    beamLen = 30
    beamDiameter = 4
    beam = cq.Workplane("XY").circle(beamDiameter / 2).extrude(beamLen)
    beamVert = beam.cut(
        c.receiver.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, beamLen))
    ).cut(c.receiver)
    # show(beamVert)
    beamHorz = beamVert.rotate((0, 0, 0), (1, 0, 0), 90).translate(
        (20, 0, beamDiameter / 2)
    )
    # show(beamHorz)

    # Create dowels
    dowel1 = c.dowelHorz().translate((40, 0, 0))
    # show(dowel1)
    dowel2 = c.dowelHorz().translate((60, 0, 0))
    # show(dowel2)

    result = beamHorz.add(beamVert).add(dowel1).add(dowel2).combine()
    show(result)

    import io

    tolerance = 0.001
    f = io.open(
        f"rectcon-tol_{tolerance:.4f}-dia_{beamDiameter:.4f}-x_{c.dowelBb.xlen:.4f}-y_{c.dowelBb.ylen:.4f}-a_{c.dowelAngle:.4f}.stl",
        "w+",
    )
    cq.exporters.exportShape(result, cq.exporters.ExportTypes.STL, f, tolerance)
    f.close()
