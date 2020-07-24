import cadquery as cq  # type: ignore

from utils import show

result = cq.Workplane("front").box(2, 2, 2).shell(-0.99)
show(result)
