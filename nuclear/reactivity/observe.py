from .patch import reactify
from .observer import Observer

STACK = []
def observe(value, restrain=None):
    STACK.append(value)
    value = reactify(value)

    if not hasattr(value, '__nuclear_props'):
        return None
    
    try:
        if hasattr(value, '__ob__') and type(value.__ob__) is Observer:
            ob = value.__ob__
        else:
            ob = Observer(value, restrain=restrain)
        return ob
    
    except AttributeError:
        return None
    finally:
        STACK.pop(-1)