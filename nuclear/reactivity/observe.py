from .patch import reactify
from .observer import Observer

STACK = []
def observe(value, restrain=None):
    if value in STACK:
        return
    
    STACK.append(value)
    value = reactify(value)
    
    try:
        if hasattr(value, '__ob__') and type(value.__ob__) is Observer:
            ob = value.__ob__
        else:
            ob = Observer(value, restrain=restrain)
        
        STACK.pop(-1)
        return ob
    
    except AttributeError:
        return None
