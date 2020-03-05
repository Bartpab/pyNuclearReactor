import types

from .observer import Observer

class Observable(object):
    def __getattribute__(self, key):
        if key == "__accessors":
            return object.__getattribute__(self, key)
        
        if hasattr(self, '__accessors'):
            accessors = object.__getattribute__(self, '__accessors')
            if key in accessors:
                return accessors[key][0](self) # Getter
        
        return object.__getattribute__(self, key)

    def __setattr__(self, key, value):
        if key is not '__accessors' and hasattr(self, '__accessors'):
            accessors = object.__getattribute__(self, '__accessors')
            if key in accessors:
                accessors[key][1](self, value) # Setter 
                return

        object.__setattr__(self, key, value)   

class ObservableList(list, Observable):
    def __init__(self, ls):
        self.extend(ls)

def is_observable(value):
    if type(value) in [list, str]: 
        return False

    return True

def observe(value, restrain=None):
    from .augment import augment
    
    # Some cTypes cannot be directly observable
    if not is_observable(value):
        return None
        
    if not isinstance(value, Observable):
        value = augment(value)
    
    if not isinstance(value, Observable):
        return None
    
    if hasattr(value, '__ob__') and type(value.__ob__) is Observer:
        ob = value.__ob__
    else:
        ob = Observer(value, restrain=restrain)

    return ob