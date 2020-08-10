from functools import reduce
from typing import List, Sequence, Tuple

import cadquery as cq  # type: ignore

from wing_utils import X, Y, dbg, show


def fattenTe(
    af: List[Tuple[float, float]], t: float, chord: float, percentChordToFatten: float,
) -> List[Tuple[float, float]]:
    """
    Fatten the trailing edge of the airfoil
      af: airfoil array of points
      t:  thickness
      c: Number of points to spread the thickness over
    """
    halfT: float = t / 2
    topTeIdx: int = 0
    btmTeIdx: int = len(af) - 1
    # dbg(
    #    f"1 len(af)={len(af)} t={t} chord={chord} %={percentChordToFatten} halfT={halfT} topTeIdx={topTeIdx} btmTeIdx={btmTeIdx} {af[topTeIdx][X]} {af[btmTeIdx][X]}"
    # )
    if af[topTeIdx][X] != af[btmTeIdx][X]:
        # dbg(f"Add an extra point to so TE is square")
        af.append((af[topTeIdx][X], af[topTeIdx][Y]))
        btmTeIdx += 1
    # dbg(
    #    f"2 len(af)={len(af)} t={t} chord={chord} %={percentChordToFatten} halfT={halfT} topTeIdx={topTeIdx} btmTeIdx={btmTeIdx} {af[topTeIdx][X]} {af[btmTeIdx][X]}"
    # )
    i: int = 0

    # Search for point less than the percentChordToFatten
    # along the top of airfoil starting at Te
    desired = chord * percentChordToFatten
    idxCurDist = 0  # Te index
    curDist = af[0][X]  # Te dist
    for i in range(0, len(af)):
        dist = af[i][X]
        if dist <= desired:
            idxCurDist = i
            curDist = dist
            break
    if idxCurDist >= len(af) - 1:
        raise Exception("Could not find top starting point")
    topIdxDist = idxCurDist
    topDist = curDist
    # dbg(f"topIdxDist={topIdxDist} topDist={topDist}")

    # Search from where we left off and find the point
    # greater than desired to find the corresponding btm point
    for i in range(idxCurDist, len(af)):
        dist = af[i][X]
        if dist >= desired:
            idxCurDist = i
            curDist = dist
            break
    if idxCurDist >= len(af) - 1:
        raise Exception("Could not find bottom starting point")
    btmIdxDist = idxCurDist
    btmDist = curDist
    # dbg(f"btmIdxDist={btmIdxDist} btmDist={btmDist}")

    # Fatten the TE "top" side of the airfoil
    ft: List[Tuple[float, float]] = []
    demomininator = chord - topDist
    for i in range(0, topIdxDist):
        curDist = af[i][X] - topDist
        v = (curDist / demomininator) * halfT
        # dbg(f"top1 i={i} v={v} af[{i}][X]={af[i][X]} af[{i}][Y]={af[i][Y]}")
        ft.append((af[i][X], af[i][Y] + v))
        # dbg(f"top2 i={i} v={v} ft[{i}][X]={ft[i][X]} ft[{i}][Y]={ft[i][Y]}")

    # Just copy the next tuples until we reach the "bottom" side to fatten
    for i in range(topIdxDist, btmIdxDist):
        ft.append((af[i][X], af[i][Y]))
        # dbg(f"copy i={i} v={v} ft[{i}][X]={ft[i][X]} ft[{i}][Y]={ft[i][Y]}")

    # Fatten the TE "bottom" side of the airfoil
    demomininator = chord - btmDist
    for i in range(btmIdxDist, len(af)):
        curDist = af[i][X] - btmDist
        v = (curDist / demomininator) * halfT
        # dbg(f"btm1 i={i} v={v} af[{i}][X]={af[i][X]} af[{i}][Y]={af[i][Y]}")
        ft.append((af[i][X], af[i][Y] - v))
        # dbg(f"btm2 i={i} v={v} ft[{i}][X]={ft[i][X]} ft[{i}][Y]={ft[i][Y]}")

    return ft


if __name__ == "__main__" or "show_object" in globals():

    from wing_utils import setCtx

    setCtx(globals())

    import airfoil as af
    from naca5305 import naca5305
    from scale import scaleListOfTuple

    airfoilSection: af.AirfoilSeq = naca5305
    chord: float = 50
    scaleFactor: float = 1 / airfoilSection[0][0]
    nAirfoil: List[Tuple[float, float]] = af.scaleListOfTuple(
        airfoilSection, scaleFactor
    )
    sAirfoil: List[Tuple[float, float]] = af.scaleListOfTuple(nAirfoil, chord)

    # fattenTe
    fTeAirfoil: List[Tuple[float, float]] = fattenTe(
        af=sAirfoil, t=0.26 * 2, chord=chord, percentChordToFatten=0.20,
    )
    airfoil = cq.Workplane("YZ").polyline(fTeAirfoil).close()
    show(airfoil, name="airfoil")
