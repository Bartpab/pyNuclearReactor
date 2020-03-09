import types
import functools

def mutant_monkey_patch(obj):
    if hasattr(obj, '__nuclear_props'):
        return
        
    obj.__nuclear_props = {}
    base_cls = obj.__class__
    
    class Patch(base_cls):        
        def __getattribute__(self, key):
            base_getattr = base_cls.__getattribute__
            try:
                properties = base_getattr(self, '__nuclear_props')
                if properties and key in properties:
                    return properties[key].get(
                       getter=functools.partial(base_getattr, self, key)
                    )
            
            except AttributeError:
                return base_getattr(self, key)
            
            finally:
                return base_getattr(self, key)
            
        def __setattr__(self, key, value):
            base_getattr = base_cls.__getattribute__
            base_setattr = base_cls.__setattr__
            
            try:
                properties = base_getattr(self, '__nuclear_props')
                if properties and key in properties:
                    properties[key].set(
                        value, 
                        getter=functools.partial(base_getattr, self, key), 
                        setter=functools.partial(base_setattr, self, key)
                    )
                    return
            
            except AttributeError:
                base_setattr(self, key, value) 
            
            finally:
                base_setattr(self, key, value) 
    
    obj.__class__ = type('Nuclear' + obj.__class__.__name__, (Patch,), {})

##########################
# Make a list observable #
##########################
class ObservableList(list, object):
    def __init__(self, ls):
        self.extend(ls)

class ObservableDict(dict, object):
    def __init__(self, d):
        self.update(d)    
        
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
  
def dict_monkey_patch(ls):
    method_props = [
        ('update', True), 
        ('items', False), 
        ('__getitem__', False), 
        ('__setitem__', True), 
        ('__delitem__', True),
        ('__iter__', False)
    ]

    for method_prop in method_props:
        setattr(ls, method_prop[0], proxy_method(ls, method_prop))  
def list_monkey_patch(ls):
    method_props = [
        ('append', True), 
        ('remove', False), 
        ('pop', False), 
        ('__getitem__', False), 
        ('__setitem__', True), 
        ('__iter__', False)
    ]

    for method_prop in method_props:
        setattr(ls, method_prop[0], proxy_method(ls, method_prop))
        
def reactify(value):
    """
        Patch the value to be observable
    """
    try:
        if type(value) is list:
            obs_ls = ObservableList(value)
            mutant_monkey_patch(obs_ls)
            list_monkey_patch(obs_ls)
            return obs_ls
        elif type(value) is dict:
            obs_dict = ObservableDict(value)
            mutant_monkey_patch(obs_dict)
            dict_monkey_patch(obs_dict)
            return obs_dict
        else:
            mutant_monkey_patch(value)
            return value  
    
    except AttributeError:
        return value
    
    except TypeError:
        return value