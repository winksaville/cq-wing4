import math
from typing import List, Sequence, Tuple

import cadquery as cq  # type: ignore

import airfoil as af
from fattenTe import fattenTe
from naca5305 import naca5305
from scale import scaleListOfTuple
from wing_utils import X, dbg, show, valid


class Wing:
    """
    Create a wing
    """

    @staticmethod
    def makeWing(
        airfoilSeq: af.AirfoilSeq,  # Sequence of points defining the airfoil
        chord: float = 50,  # Wing length LE to TE
        span: float = 100,  # Wing span from wing tip to wing tip
        incidenceAngle: float = 2.0,  # Angle in degrees of LE of wing above the TE
        dihedral=0,  # Angle in degrees of root to wing tip
        sweep=0,  # Angle of sweep back in degrees of LE
        # 0 is perpendicular to root, >0 is sweept back, <0 is sweept forward
        shellThickness: float = 0.25,  # Thickness of wing surfaces and ribs
        ribCount: int = 6,  # Number of ribs
        shortCut: bool = False,  # True to speed things up for testing
    ) -> cq.Shape:

        dihedral = math.radians(dihedral)
        sweep = math.radians(sweep)
        h: float = span / 2
        wingShellThickness: float = shellThickness
        ribThickness: float = wingShellThickness

        # Normalize, Scale, fattenTe
        fTeAirfoil = af.scaleAirfoil(
            airfoilSeq,
            chord=chord,
            teThickness=shellThickness * 2,
            percentChordToFatten=0.20,
        )

        airfoil = cq.Workplane("YZ").polyline(fTeAirfoil).close()
        dbg(f"valid(airfoil)={valid(airfoil)}")
        # show(airfoil)

        halfWing = airfoil.sweep(
            cq.Workplane("YX").spline(
                [(0, 0, 0), (h * math.sin(sweep), h, h * math.sin(-dihedral))]
            )
        )
        dbg(f"valid(halfWing)={valid(halfWing)}")
        # show(halfWing)

        fullWing: cq.Workplane
        if not shortCut:
            halfWingBb = halfWing.val().BoundingBox()
            dbg(f"ylen={halfWingBb.ylen}, zlen={halfWingBb.zlen}")

            # Create the braces which the ribs will be cut from
            braceCount: int = ribCount + 2
            braceGap: float = h / (braceCount - 1)
            bracePlates: List[cq.Shape] = []
            for i in range(0, braceCount):
                ribXPos = i * braceGap
                if i == (braceCount - 1):
                    ribXPos -= ribThickness
                bracePlate = (
                    cq.Workplane(
                        "YZ",
                        origin=(ribXPos, (halfWingBb.ylen) / 2, halfWingBb.zlen / 2),
                    ).rect(halfWingBb.ylen * 1.10, halfWingBb.zlen * 1.50)
                    # First rib is 1/2 ribThickness
                    .extrude(ribThickness if i != 0 else ribThickness / 2)
                )
                # dbg(f'{i}: braceGap={braceGap} valid(bracePlate)={valid(bracePlate)}')
                bracePlates.append(bracePlate)
                # show(bracePlate)
            dbg(f"valid(bracePlages)={valid(bracePlates)}")

            # Create the ribs
            ribs = [plate.intersect(halfWing) for plate in bracePlates]
            dbg(f"valid(ribs)={valid(ribs)}")
            # for rib in ribs: show(rib)

            halfWingCutter = (
                cq.Workplane("YZ")
                .polyline(fTeAirfoil)
                .close()
                .offset2D(-wingShellThickness, "intersection")
                .sweep(
                    cq.Workplane("YX").spline(
                        [(0, 0, 0), (h * math.sin(sweep), h, h * math.sin(-dihedral))]
                    )
                )
            )
            dbg(f"valid(halfWingCutter)={valid(halfWingCutter)}")
            # show(halfWingCutter)

            # Cut out the center of the halfWing
            halfWingHollow = halfWing.cut(halfWingCutter)
            dbg(f"valid(halfWingHollow)={valid(halfWingHollow)}")
            # show(halfWingHollow)

            # Union the ribs and wing, this is slow
            halfWingWithRibs = halfWingHollow
            for rib in ribs:
                halfWingWithRibs = halfWingWithRibs.union(rib)
            dbg(f"valid(halfWingWithRibs)={valid(halfWingWithRibs)}")
            # show(halfWingWithRibs)
            fullWing = halfWingWithRibs.mirror("YZ").union(halfWingWithRibs)
        else:
            fullWing = halfWing.mirror("YZ").union(halfWing)

        dbg(f"valid(fullWing)={valid(fullWing)}")
        # show(fullWing)

        verticalWing = fullWing.rotate((0, 0, 0), (1, 0, 0), -90)
        dbg(f"valid(verticalWing)={valid(verticalWing)}")
        # show(verticalWing)

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

    from wing_utils import setCtx

    setCtx(globals())

    shortCut: bool = True
    chord = 50
    span = 200
    incidenceAngle = 2
    dihedral = 5
    sweep = 10
    tk = 0.25
    ribCount = 0
    shortCut = False
    wing = Wing.makeWing(
        airfoilSeq=naca5305,
        chord=chord,
        span=span,
        incidenceAngle=incidenceAngle,
        dihedral=dihedral,
        sweep=sweep,
        shellThickness=tk,
        ribCount=ribCount,
        shortCut=shortCut,
    )
    show(wing)
