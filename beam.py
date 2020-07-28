import cadquery as cq  # type: ignore

from rectcon import RectCon
from utils import dbg, show

if __name__ == "__main__" or "show_object" in globals():

    c = RectCon(xLen=2.25, yLen=2.25, zLen=6)
    # show(c.receiver, ctx=globals())
    # show(c.dowel, ctx=globals())
    # show(c.dowelHorz(), ctx=globals())

    # beamLen = 30
    # beam = cq.Workplane("XY").circle(beamDiameter / 2).extrude(beamLen)
    # x = c.addReceiver(beam, ">Z")
    # show(x, ctx=globals())

    # Create beam
    beamLen = 30
    beamDiameter = 4
    beam = cq.Workplane("XY").circle(beamDiameter / 2).extrude(beamLen)
    beamVert = beam.cut(
        c.receiver.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, beamLen))
    ).cut(c.receiver)
    # show(beamVert, ctx=globals())
    beamHorz = beamVert.rotate((0, 0, 0), (1, 0, 0), 90).translate(
        (0, 0, beamDiameter / 2)
    )
    show(beamHorz, ctx=globals())

    import io

    tolerance = 0.001
    f = io.open(
        f"beam-tol_{tolerance:.4f}-dia_{beamDiameter:.4f}-len_{beamLen}-recv-x_{c.receiverBb.xlen:.4f}-y_{c.receiverBb.ylen:.4f}-z_{c.receiverBb.zlen:.4f}.stl",
        "w+",
    )
    cq.exporters.exportShape(beamHorz, cq.exporters.ExportTypes.STL, f, tolerance)
    f.close()
