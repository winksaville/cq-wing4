"""
Some scaling functions
"""

def scaleTuple(t, v):
    """Scale the elements of the tuple by v"""
    #print(f'scaleTuple: t={t} v={v}')
    return tuple(map(lambda p: p * v, t))

def scaleListOfTuple(l, v):
    """Scale the elements list of tuples by v"""
    return list(map(lambda t: scaleTuple(t, v), l))

