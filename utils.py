from functools import reduce
from typing import List, Sequence, Tuple, Union

import cadquery as cq  # type: ignore

X: int = 0
Y: int = 1
Z: int = 2


def show(o: object, ctx=None):
    """
    Show an object, support show_object from cq-editor
    otherwise does the best it can.
    """
    if o is None:
        dbg("o=None")
    elif ctx is not None and "show_object" in ctx:
        ctx["show_object"](o)
    elif isinstance(o, cq.Shape):
        dbg(f"o.val().isValid()={o.val().isValid()}")
    else:
        dbg(f"vars={vars(o)}")


def dbg(*args):
    print(*args)


def valid(wp: Union[cq.Workplane, Sequence[cq.Workplane]]) -> bool:
    if isinstance(wp, Sequence):
        return reduce(lambda value, s: value and s.val().isValid(), wp, True)
    else:
        return wp.val().isValid()


# def dbg(*args, ctx=None):
#    """
#    Output via log of cq-editor or use print
#    """
#    if ctx != None and 'log' in ctx:
#        # This outputs the first parameter plus ctx :(
#        ctx['log'](*args)
#    else:
#        print(*args)
