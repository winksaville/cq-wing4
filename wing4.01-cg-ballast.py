# Wing4.01
#
# Dimeensions mm
# Weights g


loa: float = 162
wingSpan: float = 200
wingChord: float = 50
tailSpan: float = 80
tailChord: float = 20
noseLoc: float = 30

# Weights
oaWeightNoBallast: float = 13.29 # Over All Weight
noseWeightNoBallast: float = 7.89 # Weight measured at nose
tailWeightNoBallast: float = 5.33 # Weight measured at tail
oacWeightNoBallast: float = noseWeightNoBallast + tailWeightNoBallast

cgNoBallast: float = (loa * tailWeightNoBallast) / oacWeightNoBallast

print(f"cgNoBallast={cgNoBallast:.2f}")

cgPct: float = 0.30
cgLoc: float = cgPct * wingChord
ballastOffset: float = -30
ballast: float = ((cgNoBallast - (cgLoc + noseLoc)) * oacWeightNoBallast) / ((cgLoc + noseLoc) - ballastOffset)

print(f"cgLoc={cgLoc:.2f} ballast={ballast:.2f}")
