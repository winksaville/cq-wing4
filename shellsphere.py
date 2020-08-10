import cadquery as cq  # type: ignore

from wing_utils import show

result = cq.Workplane("front").sphere(2).shell(-1.9999)
show(result)
