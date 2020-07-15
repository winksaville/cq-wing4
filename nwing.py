from naca5305 import naca5305
from scale import scaleListOfTuple
from fattenTe import fattenTe

import cadquery as cq # type: ignore

#import sys
#print(f'sys.path={sys.path}')


chord: float = 50 
h = 100

# Normalize, Scale, fattenTe
scaleFactor = 1/naca5305[0][0]
nNaca5305 = scaleListOfTuple(naca5305, scaleFactor)
sNaca5305 = scaleListOfTuple(nNaca5305, chord)
fNaca5305 = fattenTe(sNaca5305, 0.25, 10)
#fNaca5305 = sNaca5305

# Create the 2D airfoil then extrude
#airfoil = cq.Workplane("YZ").spline(fNaca5305).close()
airfoil = cq.Workplane("YZ").polyline(fNaca5305).close()
halfWing = airfoil.extrude(h)
halfWingBb = halfWing.val().BoundingBox()

# If workplane is >= 0.9902054 FAILS
#splitWing = halfWing.faces("<Y").workplane(-chord*0.9902054).split(keepTop=True, keepBottom=False)
splitWingA = halfWing.faces("<Y").workplane(-chord*0.50).split(keepTop=True, keepBottom=False)
#show_object(splitWingA)
splitWing = splitWingA.faces(">Y").workplane(-chord*0.15).split(keepTop=True, keepBottom=False)
#show_object(splitWing)

#halfWingShell = splitWing.shell(-0.29)
halfWingShell = splitWing.shell(-0.72) # OK
#alfWingShell = splitWing.shell(-0.196) # OK
show_object(halfWingShell)


# Split the wing to determine where it can shelled. As it turns
# if a spline is used out the problem is in the leading edge
# AND:

# If workplane is >= 0.9902054 FAILS
#splitWing = halfWing.faces(">Y").workplane(-chord*0.9902054).split(keepTop=True, keepBottom=False)

## if workplace is < -chord*0.9902053 SUCCEEDS!
#splitWing = halfWing.faces(">Y").workplane(-chord*0.9902053).split(keepTop=True, keepBottom=False)
##splitWing = halfWing.faces(">Y").workplane(-chord*0.8).split(keepTop=True, keepBottom=False)
#
#log(f'splitWing.isValid()={splitWing.val().isValid()}')
##show_object(splitWing)
#splitWingShell = splitWing.shell(-0.0270)
#show_object(splitWingShell)

# Shell the halfWing with splined airfoil and use small
# positive values for thickness shelling works. If the
# thickness too small or negative it FAILS:
#alfWingShell = halfWing.shell(0.0001) # StdFail_NotDone: BRep_API: command not done
#alfWingShell = halfWing.shell(0.00010000000000000001) # StdFail_NotDone: BRep_API: command not done
#alfWingShell = halfWing.shell(0.0001000000000000000115) # StdFail_NotDone: BRep_API: command not done
#alfWingShell = halfWing.shell(0.0001000000000000000116) # OK
#alfWingShell = halfWing.shell(0.0001000000000000001) # OK
#alfWingShell = halfWing.shell(0.000100000001) # OK
#alfWingShell = halfWing.shell(0.00010000001) # OK
#alfWingShell = halfWing.shell(0.00010001) # OK
#alfWingShell = halfWing.shell(0.0001001) # OK
#alfWingShell = halfWing.shell(0.00012) # OK
#alfWingShell = halfWing.shell(0.0005) # OK
#alfWingShell = halfWing.shell(0.005) # OK
#alfWingShell = halfWing.shell(0.001) # OK
#alfWingShell = halfWing.shell(0.01) # OK
#alfWingShell = halfWing.shell(0) # StdFail_NotDone: BRep_API: command not done
#alfWingShell = halfWing.shell(-0.000000000000000000000001) # StdFail_NotDone: BRep_API: command not done
#alfWingShell = halfWing.shell(-0.000002) # StdFail_NotDone: BRep_API: command not done

#show_object(halfWingShell)
#show_object(halfWing)
#show_object(airfoil)

