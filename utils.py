import sys
from functools import reduce
from math import radians
from typing import List, Sequence, Tuple, Union

import cadquery as cq  # type: ignore

X: int = 0
Y: int = 1
Z: int = 2

_ctx = None


def setCtx(ctx) -> None:
    """
    Call setCtx() with globals() prior to using
    show or dbg methods when using cq-editor.
    """
    global _ctx
    _ctx = ctx


if "cq_editor" in sys.modules:
    # from __main__ import self as _cq_editor
    from logbook import info as _cq_log

    def show(o: object, name=None):
        if _ctx is None:
            raise ValueError("utils.setCtx was not called")
        if _ctx["show_object"] is None:
            raise ValueError("_ctx['show_object'] is not available")
        _ctx["show_object"](o, name=name)
        # _cq_editor.components["object_tree"].addObject(o) # Does not work

    def dbg(*args):
        _cq_log(*args)


else:

    def show(o: object, name=None):
        if name is None:
            name = str(id(o))
        if o is None:
            dbg(f"{name}: o=None")
        elif isinstance(o, cq.Workplane):
            dbg(f"{name}: valid={o.val().isValid()} {vars(o)}")
        else:
            dbg(vars(o))

    def dbg(*args):
        print(*args)


def translate_2d(
    lst: Sequence[Tuple[float, float]], t: Tuple[float, float]
) -> List[Tuple[float, float]]:
    """Translate a 2D obect to a different location on a plane"""
    return [(loc[X] + t[X], loc[Y] + t[Y]) for loc in lst]


def xDist_2d(line: Tuple[Tuple[float, float], Tuple[float, float]]) -> float:
    return line[1][X] - line[0][X]


def yDist_2d(line: Tuple[Tuple[float, float], Tuple[float, float]]) -> float:
    return line[1][Y] - line[0][Y]


def slope_using_dist_2d(xDist: float, yDist: float) -> float:
    if xDist == 0:
        # What about nan's and -0 this is why there is no math.sign
        # See: https://stackoverflow.com/a/16726462
        slope = (1 if yDist >= 0.0 else -1) * radians(90)
    else:
        slope = yDist / xDist

    return slope


def slope_2d(line: Tuple[Tuple[float, float], Tuple[float, float]]) -> float:
    return slope_using_dist_2d(xDist_2d(line), yDist_2d(line))


def slope_yIntercept_2d(
    line: Tuple[Tuple[float, float], Tuple[float, float]]
) -> Tuple[float, float]:
    """
    Return the two tuple (yIntercept, Slope) of line
    """

    # Line formula: y = (slope * x) + b
    # b = y - (slope * x)
    # yIntercept = b when x == 0
    slope = slope_2d(line)
    yIntercept = line[0][Y] - (slope * line[0][X])

    return (slope, yIntercept)


def split_2d(
    lst: Sequence[Tuple[float, float]],
    line: Tuple[Tuple[float, float], Tuple[float, float]],
    retAbove=True,
) -> List[Tuple[float, float]]:
    """
    Split the list defining a 2D object using line.
    If retAbove it True return all points >= line else all point <= line

    :param lst: is a sequence of 2D point tuples
    :param line: a two tuple of 2D point tuples
    :param retAbove:
    """
    # print(f"slipt_2d:+ lst={lst} line={line} retAbove={retAbove}")

    slope, yIntercept = slope_yIntercept_2d(line)

    # print(f"yIntercept={yIntercept}")

    # Formula for a 2d line is y = slope * x + yYntercept
    # Solve for lineY for each p[X]:
    #   lineY = ((slope * p[X]) + yIntercept)
    if retAbove:
        # Valid point for newList if p[Y] >= lineY, otherwise skip
        newList = [p for p in lst if p[Y] >= ((slope * p[X]) + yIntercept)]
    else:
        # Valid point for newList if p[Y] <= lineY, otherwise skip
        newList = [p for p in lst if p[Y] <= ((slope * p[X]) + yIntercept)]
    # print(f"slipt_2d: newList={newList}")

    # print(f"slipt_2d:- lst={lst} line={line} retAbove={retAbove}")
    return newList


def valid(wp: Union[cq.Workplane, Sequence[cq.Workplane]]) -> bool:
    if isinstance(wp, Sequence):
        return reduce(lambda value, s: value and s.val().isValid(), wp, True)
    else:
        return wp.val().isValid()


def updatePending(wp: cq.Workplane) -> cq.Workplane:
    """
    Clear pendingWires and pendingEdges and then add
    objects that are wires or edges to the appropriate
    pending list. Another way to fix this would be to
    add a parameter to toPending which would do the
    clear before the extending operation.

    Fix cq bug https://github.com/CadQuery/cadquery/issues/421
    """
    wp.ctx.pendingWires = []
    wp.ctx.pendingEdgs = []
    return wp.toPending()
