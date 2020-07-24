import cadquery as cq  # type: ignore

chord: float = 50
h = 100

airfoil = cq.Workplane("YZ").ellipse(chord, 5)
halfWing = airfoil.extrude(h)

# Shell the halfWing
# halfWingShell = halfWing.shell(-2.8) # ValueError: Null TopoDS_Shape object
# halfWingShell = halfWing.shell(-2.7) # Standard_NullObject: Brep_Tool:: TopoDS_Vertex hasn't gp_Pnt
# halfWingShell = halfWing.shell(-2.6) # StdFail_NotDone: BRep_API: command not done
# halfWingShell = halfWing.shell(-2.55) # ValueError: Null TopoDS_Shape object
# halfWingShell = halfWing.shell(-2.5496) # ValueError: Null TopoDS_Shape object
# halfWingShell = halfWing.shell(-2.54955) # ValueError: Null TopoDS_Shape object
# halfWingShell = halfWing.shell(-2.54954) # ValueError: Null TopoDS_Shape object
# halfWingShell = halfWing.shell(-2.549539) # ValueError: Null TopoDS_Shape object
# halfWingShell = halfWing.shell(-2.549538) # ValueError: Null TopoDS_Shape object
# halfWingShell = halfWing.shell(-2.5495378) # ValueError: Null TopoDS_Shape object
# halfWingShell = halfWing.shell(-2.549537799) # ValueError: Null TopoDS_Shape object
# halfWingShell = halfWing.shell(-2.549537796) # ValueError: Null TopoDS_Shape object
halfWingShell = halfWing.shell(-2.549537795)  # OK
# halfWingShell = halfWing.shell(-2.54953779) # OK
# halfWingShell = halfWing.shell(-2.54953777) # OK
# halfWingShell = halfWing.shell(-2.5495376) # OK
# halfWingShell = halfWing.shell(-2.5495375) # OK
# halfWingShell = halfWing.shell(-2.549537) # OK
# halfWingShell = halfWing.shell(-2.549535) # OK
# halfWingShell = halfWing.shell(-2.54952) # OK
# halfWingShell = halfWing.shell(-2.5495) # OK
# halfWingShell = halfWing.shell(-2.54) # OK
# halfWingShell = halfWing.shell(-2.5) # OK
# halfWingShell = halfWing.shell(-2.4) # OK
# halfWingShell = halfWing.shell(-2.3) # OK
# halfWingShell = halfWing.shell(-1) # OK
show_object(halfWingShell)
