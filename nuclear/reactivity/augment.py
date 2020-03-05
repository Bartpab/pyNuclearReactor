
def augment(value):
    """
        Patch the value to be observable
    """
    from .observe import ObservableList, Observable, is_observable
    
    if issubclass(type(value), Observable):
        return value
    
    if not is_observable(value) and type(value) is not list:
        return value
    
    try:
        if not isinstance(value, Observable) and hasattr(value, '__dict__'):
            ObservablePatch = type(value.__class__.__name__, (value.__class__, Observable), {})
            value.__class__ = ObservablePatch   
            return value
        
        elif type(value) is list:
            return ObservableList(value)
    
    except TypeError:
        return value
    
    return value
    
def proxy_method(self, method_prop):
    method_name, is_inserting = method_prop
    method = getattr(self, method_name)
    
    def proxy(*args, **kwargs):
        ob = self.__ob__
        result = method(*args, **kwargs)
        
        if is_inserting:
            ob.observe_list(args)
        
        ob.dep.notify()
    
    return proxy
    
def augment_list(ls):
    method_props = [('append', True), ('remove', False), ('pop', False), ('__getitem__', False), ('__setitem__', True), ('__iter__', False)]

    for method_prop in method_props:
        setattr(ls, method_prop[0], proxy_method(ls, method_prop))
        