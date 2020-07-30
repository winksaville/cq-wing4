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


loa: float = 162 # LOA
wingSpan: float = 200
wingChord: float = 50
tailSpan: float = 80
tailChord: float = 20

# Weights
oaWeight: float = 13.49 # Over All Weight
noseWeight: float = 7.86 # Weight measured at nose
tailWeight: float = 5.44 # Weight measured at tail
oacWeight: float = noseWeight + tailWeight
noseLen: float = 30
cgNoBallast: float = (loa * tailWeight) / (oacWeight * noseLen)


cgPct: float = 0.30
cgLoc: float = cgPct * wingChord # CG
ballastOffset: float = -60 # BO
ballast: float = ((cgNoBallast - cgLoc) * oacWeight) / (cgLoc + ballastOffset)

print(
f"""noseWeight={noseWeight}g
tailWeight={tailWeight}g
oacWeight={oacWeight}g
oaWeight={oaWeight}g
ballastOffset={ballastOffset}mm from LE wing
ballast={ballast:.2f}g
cgLoc={cgLoc:.2f}mm from LE wing
cgPct={cgPct}%""")
