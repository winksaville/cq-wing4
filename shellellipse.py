import cadquery as cq
result = (
    cq.Workplane("front")
    .ellipse(2, 4)
    .extrude(2)
    .shell(-1.5)
)
show_object(result)
