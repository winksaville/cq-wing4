import math
from functools import reduce
from typing import List, Sequence, Tuple

import cadquery as cq  # type: ignore

import airfoil as af
from fattenTe import fattenTe
from naca5305 import naca5305
from scale import scaleListOfTuple
from utils import X, dbg, show, valid


class Wing:
    """
    Create a wing
    """

    @staticmethod
    def makeWing(
        airfoilSeq: af.AirfoilSeq,  # Sequence of points defining the airfoil
        incidenceAngle: float = 2.0,  # Angle of LE of wing above the TE
        shellThickness: float = 0.25,  # Thickness of wing surfaces and ribs
        ctx: object = None,  # Context used for show and dbg
    ) -> cq.Shape:

        dihederal = math.radians(5)
        sweep = math.radians(0)
        h: float = 100
        chord: float = 50
        wingShellThickness: float = shellThickness
        ribThickness: float = wingShellThickness

        # Normalize, Scale, fattenTe
        fTeAirfoil = af.scaleAirfoil(airfoilSeq, chord, shellThickness * 2, 0.20)

        airfoil = cq.Workplane("YZ").polyline(fTeAirfoil).close()
        dbg(f"valid(airfoil)={valid(airfoil)}")
        # show(airfoil, ctx)

        halfWing = airfoil.sweep(
            cq.Workplane("YX").spline(
                [(0, 0, 0), (h * math.sin(sweep), h, h * math.sin(-dihederal))]
            )
        )
        dbg(f"valid(halfWing)={valid(halfWing)}")
        # show(halfWing, ctx)

        # Shell the halfWing
        # halfWingShell = halfWing.shell(-0.25)
        # show(halfWingShell, ctx)

        halfWingBb = halfWing.val().BoundingBox()
        dbg(f"ylen={halfWingBb.ylen}, zlen={halfWingBb.zlen}")

        # Create the braces which the ribs will be cut from
        braceCount = 8
        braceGap: float = h / (braceCount - 1)
        bracePlates: Sequence[cq.Shape] = []
        for i in range(0, braceCount):
            ribXPos = i * braceGap
            if i == (braceCount - 1):
                ribXPos -= ribThickness
            bracePlate = (
                cq.Workplane(
                    "YZ", origin=(ribXPos, (halfWingBb.ylen) / 2, halfWingBb.zlen / 2)
                ).rect(halfWingBb.ylen * 1.10, halfWingBb.zlen * 1.50)
                # First rib is 1/2 ribThickness
                .extrude(ribThickness if i != 0 else ribThickness / 2)
            )
            # dbg(f'{i}: braceGap={braceGap} valid(bracePlate)={valid(bracePlate)}')
            bracePlates.append(bracePlate)
            # show(bracePlate, ctx)
        dbg(f"valid(bracePlages)={valid(bracePlates)}")

        # Create the ribs
        ribs = [plate.intersect(halfWing) for plate in bracePlates]
        dbg(f"valid(ribs)={valid(ribs)}")
        # for rib in ribs: show(rib, ctx)

        halfWingCutter = (
            cq.Workplane("YZ")
            .polyline(fTeAirfoil)
            .close()
            .offset2D(-wingShellThickness, "intersection")
            .sweep(
                cq.Workplane("YX").spline(
                    [(0, 0, 0), (h * math.sin(sweep), h, h * math.sin(-dihederal))]
                )
            )
        )
        dbg(f"valid(halfWingCutter)={valid(halfWingCutter)}")
        # show(halfWingCutter, ctx)

        # Cut out the center of the halfWing
        halfWingHollow = halfWing.cut(halfWingCutter)
        dbg(f"valid(halfWingHollow)={valid(halfWingHollow)}")
        # show(halfWingHollow, ctx)

        # Union the ribs and wing, this is slow
        halfWingWithRibs = halfWingHollow
        for rib in ribs:
            halfWingWithRibs = halfWingWithRibs.union(rib)
        dbg(f"valid(halfWingWithRibs)={valid(halfWingWithRibs)}")
        # show(halfWingWithRibs, ctx)

        fullWing = halfWingWithRibs.mirror("YZ").union(halfWingWithRibs)
        dbg(f"valid(fullWing)={valid(fullWing)}")
        # show(fullWing, ctx)

        verticalWing = fullWing.rotate((0, 0, 0), (1, 0, 0), -90)
        dbg(f"valid(verticalWing)={valid(verticalWing)}")
        # show(verticalWing, ctx)

        # Translate so TE is at the origin
        wingTranslated = verticalWing.translate(
            (0, 0, fTeAirfoil[-1][X] + (h * math.sin(sweep)))
        )
        dbg(f"valid(wingTranslated)={valid(wingTranslated)}")

        # Rotate by incidence angle
        wing = wingTranslated.rotate((0, 0, 0), (1, 0, 0), -incidenceAngle)
        dbg(f"valid(wing)={valid(wing)}")
        return wing


if __name__ == "__main__" or "show_object" in globals():
    w = Wing.makeWing(naca5305, shellThickness=0.20)
    show(w, ctx=globals())
