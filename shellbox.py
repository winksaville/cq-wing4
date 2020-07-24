import cadquery as cq  # type: ignore

result = cq.Workplane("front").box(2, 2, 2).shell(-0.99)
show_object(result)
