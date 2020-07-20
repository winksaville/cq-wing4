import cadquery as cq # type: ignore
result = cq.Workplane("front").sphere(2).shell(-1.9999)
show_object(result)

