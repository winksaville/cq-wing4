from scale import scaleListOfTuple
from fattenTe import fattenTe
import cadquery as cq # type: ignore
from typing import List, Sequence, Tuple, Iterable


def show(o: object, ctx=None):
    """
    Show an object, support show_object from cq-editor
    otherwise does the best it can.
    """
    if o == None:
        dbg('o=None')
    elif ctx != None and 'show_object' in ctx:
        ctx['show_object'](o)
    elif isinstance(o, cq.Shape):
        dbg(f'o.val().isValid()={o.val().isValid()}')
    else:
        dbg(f'vars={vars(o)}')

def dbg(*args):
    print(*args)

#def dbg(*args, ctx=None):
#    """
#    Output via log of cq-editor or use print
#    """
#    if ctx != None and 'log' in ctx:
#        # This outputs the first parameter plus ctx :(
#        ctx['log'](*args)
#    else:
#        print(*args)

def scaleAirfoil(
    airFoil: Sequence[Tuple[float, float]],
    chord: float,
    teThickness: float,
    percentChordToFattenTe: float = 20,
) -> List[Tuple[float, float]]:
    """
    Normalize, Scale, fattenTe an airfoil
    """
    scaleFactor: float = 1/airFoil[0][0]
    nAirfoil: List[Tuple[float, float]] = scaleListOfTuple(airFoil, scaleFactor)
    sAirfoil: List[Tuple[float, float]] = scaleListOfTuple(nAirfoil, chord)
    fAirfoil: List[Tuple[float, float]] = fattenTe(sAirfoil, teThickness, round(chord * percentChordToFattenTe))

    return fAirfoil
