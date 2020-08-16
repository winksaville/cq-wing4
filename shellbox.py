import cadquery as cq

from wing_utils import show

result = cq.Workplane("front").box(2, 2, 2).shell(-0.99)
show(result)
