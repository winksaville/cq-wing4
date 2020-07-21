import cadquery as cq # type: ignore

def show(o: object, ctx=None):
    """
    Show an object, support show_object from cq-editor
    otherwise does the best it can.
    """
    if ctx != None and 'show_object' in ctx:
        ctx['show_object'](o)
    #elif 'show_object' in globals():
    #    show_object(o)
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
