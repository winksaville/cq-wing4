import cadquery as cq  # type: ignore
from rectcon import RectCon

from utils import dbg, show

if __name__ == "__main__" or "show_object" in globals():

    # Create dowel
    c = RectCon(xLen=2.25, yLen=2.25, zLen=6)
    dowel = c.dowelHorz()
    show(dowel, ctx=globals())

    import io

    tolerance = 0.001
    f = io.open(
        f"dowel-tol_{tolerance:.4f}-x_{c.dowelBb.xlen:.4f}-y_{c.dowelBb.ylen:.4f}-z_{c.dowelBb.zlen:.4f}.stl",
        "w+",
    )
    cq.exporters.exportShape(dowel, cq.exporters.ExportTypes.STL, f, tolerance)
    f.close()
