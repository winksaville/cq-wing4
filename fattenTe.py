from typing import Tuple, List

def fattenTe(af: List[Tuple[float, float]], t: float, count: int) -> List[Tuple[float, float]]:
    """
    Fatten the trailing edge of the airfoil
      af: airfoil array of points
      t:  thickness
      c: Number of points to spread the thickness over
    """
    halfT: float = t / 2
    units: float = halfT / count
    topTeIdx: int = 0
    btmTeIdx: int = len(af) - 1
    X: int = 0
    Y: int = 1
    #print(f'1 len(af)={len(af)} t={t} count={count} halfT={halfT} units={units} topTeIdx={topTeIdx} btmTeIdx={btmTeIdx} {af[topTeIdx][X]} {af[btmTeIdx][X]}')
    if af[topTeIdx][X] != af[btmTeIdx][X]:
        # Add an extra point so that te is square not a point.
        af.append((af[topTeIdx][X], af[topTeIdx][Y]))
        btmTeIdx += 1
    #print(f'2 len(af)={len(af)} t={t} count={count} halfT={halfT} units={units} topTeIdx={topTeIdx} btmTeIdx={btmTeIdx} {af[topTeIdx][X]} {af[btmTeIdx][X]}')
    ft: List[Tuple[float, float]] = []
    i: int
    for i in range(0, count):
        v = (count - i) * units
        #print(f'i={i} v={v} af[{i}][X]={af[i][X]} af[{i}][Y]={af[i][Y]}')
        ft.append((af[i][X], af[i][Y] + v))
        #print(f'i={i} v={v} ft[{i}][X]={ft[i][X]} ft[{i}][Y]={ft[i][Y]}')

    for i in range(count, len(af) - count):
        ft.append((af[i][X], af[i][Y]))
        #print(f'i={i} v={v} ft[{i}][X]={ft[i][X]} ft[{i}][Y]={ft[i][Y]}')

    for i in range(len(af) - count, len(af)):
        v = (i - (len(af) - count) + 1) * units
        #print(f'i={i} v={v} af[{i}][X]={af[i][X]} af[{i}][Y]={af[i][Y]}')
        ft.append((af[i][X], af[i][Y] - v))
        #print(f'i={i} v={v} ft[{i}][X]={ft[i][X]} ft[{i}][Y]={ft[i][Y]}')

    return ft
