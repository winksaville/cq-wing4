import math

import cadquery as cq # type: ignore

from typing import List, Sequence, Tuple

import utils as ut

class ElipCon:
    """
    An Ellipitical Connector
    """

    @staticmethod
    def make(
        xLength: float,
        yLength: float,
        length: float,
        ctx: object=None,
    ) -> cq.Shape:
        ut.dbg(f'Elip.make: xLength={xLength} yLength={yLength} length={length}')

        e = (
            cq.Workplane("XY", origin=(0, 0, 0))
                .ellipse(xLength/2, yLength/2)
                .extrude(length)
        )
        eBb = e.val().BoundingBox()
        ut.dbg(f'eBb: xlen={eBb.xlen} ylen={eBb.ylen}')

        c = e
        cBb = c.val().BoundingBox()
        ut.dbg(f'cBb: xlen={cBb.xlen} ylen={cBb.ylen}')
        return c

if __name__ == '__main__' or 'show_object' in globals():
    c = ElipCon.make(xLength=2, yLength=4, length=8)
    ut.show(c, ctx=globals())
