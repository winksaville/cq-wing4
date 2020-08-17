"""
Some scaling functions
"""

from typing import List, Sequence, Tuple, cast


def scaleTupleByTuple(t: Tuple[float, ...], v: Tuple[float, ...]) -> Tuple[float, ...]:
    """
    Scale the elements of the tuple t by the corresponding elements of tuple v.
    The length of the t and v must be the same
    """
    # print(f'scaleTupleByTuple: t={t} v={v}')
    assert len(t) == len(v)
    return tuple(et * v[i] for i, et in enumerate(t))


def scaleListOfTupleByTuple(
    lst: Sequence[Tuple[float, ...]], v: Tuple[float, ...]
) -> List[Tuple[float, ...]]:
    """
    Scale the elements list of tuples by tuple v.
    The length of the tuples must be the same
    """
    # There is probably a more Pythonic way to do this
    result: List[Tuple[float, ...]] = []
    for t in map(lambda t: scaleTupleByTuple(t, v), lst):
        result.append(cast(Tuple[float, ...], tuple(n for n in t)))
    return result


def scaleTuple(t: Tuple[float, ...], v: float) -> Tuple[float, ...]:
    """Scale the elements of the tuple by v"""
    # print(f'scaleTuple: t={t} v={v}')
    return tuple(i for i in map(lambda p: p * v, t))


def scaleListOfTuple(
    lst: Sequence[Tuple[float, float]], v: float
) -> List[Tuple[float, float]]:
    """Scale the elements list of tuples by v"""
    # There is probably a more Pythonic way to do this
    result: List[Tuple[float, float]] = []
    for t in map(lambda t: scaleTuple(t, v), lst):
        result.append(cast(Tuple[float, float], tuple(n for n in t)))
    return result
