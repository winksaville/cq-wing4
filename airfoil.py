from typing import Iterable, List, NewType, Sequence, Tuple, cast

import cadquery as cq  # type: ignore

from fattenTe import fattenTe
from scale import scaleListOfTuple

AirfoilSeq = NewType('AirfoilSeq', Sequence[Tuple[float, float]])
AirfoilList = NewType('AirfoilList', List[Tuple[float, float]])

def scaleAirfoil(
    airFoil: AirfoilSeq,
    chord: float,
    teThickness: float,
    percentChordToFattenTe: float = 20,
) -> AirfoilList:
    """
    Normalize, Scale, fattenTe an airfoil
    """
    scaleFactor: float = 1/airFoil[0][0]
    nAirfoil: List[Tuple[float, float]] = scaleListOfTuple(airFoil, scaleFactor)
    sAirfoil: List[Tuple[float, float]] = scaleListOfTuple(nAirfoil, chord)
    fAirfoil: AirfoilList = cast(AirfoilList, fattenTe(sAirfoil, teThickness, round(chord * percentChordToFattenTe)))

    return fAirfoil
