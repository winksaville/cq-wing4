import sys
from functools import reduce
from typing import List, Sequence, Tuple, Union

import cadquery as cq  # type: ignore

X: int = 0
Y: int = 1
Z: int = 2

if "cq_editor" in sys.modules:
    from __main__ import self as _cq_editor
    from logbook import info as _cq_log

    def show(o: object):
        _cq_editor.components["object_tree"].addObject(o)

    def dbg(*args):
        _cq_log(*args)


else:

    def show(o: object):
        if o is None:
            dbg("o=None")
        elif isinstance(o, cq.Workplane):
            for i, thing in enumerate(o.objects):
                dbg(f"{i}: valid={o.val().isValid()} {vars(thing)}")
        else:
            dbg(vars(o))

    def dbg(*args):
        print(*args)


def valid(wp: Union[cq.Workplane, Sequence[cq.Workplane]]) -> bool:
    if isinstance(wp, Sequence):
        return reduce(lambda value, s: value and s.val().isValid(), wp, True)
    else:
        return wp.val().isValid()
