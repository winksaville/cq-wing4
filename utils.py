import sys
from functools import reduce
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


# Not sure how to "translate2d" natively in cadquery
def translate2d(
    lst: Sequence[Tuple[float, float]], t: Tuple[float, float]
) -> List[Tuple[float, float]]:
    """Translate a 2D obect to a different location on a plane"""
    return [(loc[X] + t[X], loc[Y] + t[Y]) for loc in lst]


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
