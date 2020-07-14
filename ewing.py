import cadquery as cq # type: ignore

chord: float = 50 
h = 100

airfoil = (
    cq.Workplane("YZ")
    .ellipse(chord, 5)
)

halfWing = (
    airfoil
    .extrude(h)
)

# Shell the halfWing
halfWingShell = halfWing.shell(-0.1)
#show_object(halfWingShell)
