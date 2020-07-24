import math
from copy import copy, deepcopy
from dataclasses import dataclass
from typing import List, Sequence, Tuple

import cadquery as cq  # type: ignore

import utils as ut


class RectCon:
    """
    An Rectangular Connector
    """

    femaleCutter: cq.Shape
    femaleBb: cq.Shape

    male: cq.Shape
    maleBb: cq.Shape

    def __init__(
        self,
        zLen: float = 10,
        xLen: float = 4,
        yLen: float = 4,
        fillets = 0.250,
        ctx: object=None,
    ) -> None:
        ut.dbg(f'RectCon.init: xLen={xLen} yLen={yLen} zLen={zLen}')


        r = (
            cq.Workplane("XY")
            .rect(xLen, yLen)
            .extrude(zLen)
            .edges(">Z")
            .fillet(fillets)
        )
        rBb = r.val().BoundingBox()
        ut.dbg(f'rBb: xlen={rBb.xlen} ylen={rBb.ylen} zlen={rBb.zlen}')
        #ut.show(e, ctx=globals())

        self.male = r
        self.maleBb = self.male.val().BoundingBox()
        ut.dbg(f'maleBb: xlen={self.maleBb.xlen} ylen={self.maleBb.ylen} zlen={self.maleBb.zlen}')

        self.female = r
        self.femaleBb = self.female.val().BoundingBox()
        ut.dbg(f'femaleBb: xlen={self.femaleBb.xlen} ylen={self.femaleBb.ylen} zlen={self.maleBb.zlen}')


if __name__ == '__main__' or 'show_object' in globals():
    @dataclass
    class Ellipse:
        xLen: float
        yLen: float

        def xAxis(self):
            return self.xLen / 2

        def yAxis(self):
            return self.yLen / 2

    c = RectCon()
    #ut.show(c.male, ctx=globals())

    bodyEllipse2d = Ellipse(xLen=8, yLen=12);

    bodyLen = 30
    body = (
        cq.Workplane("XY")
        .ellipse(bodyEllipse2d.xAxis(), bodyEllipse2d.yAxis())
        .extrude(bodyLen)
    )
    body1 = body.cut(c.female.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, bodyLen))).cut(c.female)
    #ut.show(body1, ctx=globals())

    body2 = body1.translate((20, 0, 0))
    #ut.show(body2, ctx=globals())

    stick1 = (
        c.male
        .rotate((0, 0, 0), (1, 0, 0), 180)
        .union(c.male)
        .translate((0, 0, c.maleBb.zlen))
    )
    stick1 = stick1.translate((40, 0, 0))
    #ut.show(stick1, ctx=globals())
    stick2 = stick1.translate((20, 0, 0))
    #ut.show(stick2, ctx=globals())

    bodies = (
        body1.add(body2)
        .combine()
        .rotate((0, 0, 0), (1, 0, 0), 90)
        .translate((0, 0, bodyEllipse2d.yLen / 2))
    )
    sticks = (
        stick1.add(stick2)
        .combine()
        .rotate((0, 0, 0), (1, 0, 0), 90)
        .translate((0, 0, c.maleBb.ylen / 2))
    )
    result = (
        bodies.add(sticks)
        .combine()
    )
    ut.show(result)

    import io
    tolerance=0.001;
    f = io.open(f'bodies-sticks-tol_{tolerance}.stl', 'w+')
    cq.exporters.exportShape(result, cq.exporters.ExportTypes.STL, f, tolerance)
    f.close()
