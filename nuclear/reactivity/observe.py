from .mutagen import mutate
from .observer import Observer

STACK = []
def observe(value, restrain=None):
    STACK.append(value)
    value = mutate(value)

    if not hasattr(value, '__nuclear_props'):
        return None

    if hasattr(value, '__ob__') and type(value.__ob__) is Observer:
        ob = value.__ob__
    
    else:
        ob = Observer(value, restrain=restrain)
    
    STACK.pop(-1)
    
    return ob
        