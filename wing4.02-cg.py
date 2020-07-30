#!/usr/bin/env python3
# Wing4.01
#
# Dimeensions mm
# Weights g
#
# Based on:
# |<---------------- LOA -------------->|
# |<-BO->|<-CG->|                       |
# |      |      |                 ______
# |                               |    |
#        <==========>             |    |
# ------->###########<************|____|
#
# ------ ::= "nose"
# >####< ::= "cabin"
# >****< ::= "tail beam"
# <====> ::= "wing"


loa: float = 192 # LOA
wingSpan: float = 200
wingChord: float = 50
tailSpan: float = 80
tailChord: float = 20

# Weights
oaWeight: float = 14.91 # Over All Weight
noseWeight: float = 8.15 # Weight measured at nose
tailWeight: float = 6.77 # Weight measured at tail
oacWeight: float = noseWeight + tailWeight
ballastOffset: float = -60  # BO
ballast: float = 1.43

cgLoc: float = ((tailWeight * loa) / oacWeight) + ballastOffset # CG
cgPct: float = cgLoc / wingChord * 100

print(
f"""noseWeight={noseWeight}g
tailWeight={tailWeight}g
oacWeight={oacWeight}g
oaWeight={oaWeight}g
ballastOffset={ballastOffset} from LE wing
ballast={ballast:.2f}g
cgLoc={cgLoc:.2f}mm from LE wing
cgPct={cgPct:.2f}%""")

