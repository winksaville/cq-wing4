import cadquery as cq  # type: ignore

from utils import show

result = cq.Workplane("front").ellipse(2, 4).extrude(2).shell(-1.5)
show(result)
