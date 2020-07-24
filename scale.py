"""
Some scaling functions
"""

from typing import List, Sequence, Tuple, cast


def scaleTuple(t: Tuple[float, ...], v: float) -> Tuple[float, ...]:
    """Scale the elements of the tuple by v"""
    #print(f'scaleTuple: t={t} v={v}')
    return tuple(i for i in map(lambda p: p * v, t))

def scaleListOfTuple(l: Sequence[Tuple[float, float]], v: float) -> List[Tuple[float, float]]:
    """Scale the elements list of tuples by v"""
    # There is probably a more Pythonic way to do this
    result: List[Tuple[float, float]] = []
    for t in map(lambda t: scaleTuple(t, v), l):
        result.append(cast(Tuple[float, float], tuple(n for n in t)))
    return result
