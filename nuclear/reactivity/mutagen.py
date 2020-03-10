import types
import functools

_monkey_patch_index = 0
_not_set            = object ()

def mutant_patch_prop(prop, name):
    if name.startswith("$__nuclear_prop_"):
        return
        
    global _monkey_patch_index, _not_set
    
    attr_name = '$__nuclear_prop_{}'.format (_monkey_patch_index)
    _monkey_patch_index += 1
    
    if prop is None:
        base_getter = lambda self: getattr(self, attr_name)
        base_setter = lambda self, value: setattr(self, attr_name, value)
        
    else:
        # Non-data descriptor...
        if not hasattr(prop, '__set__'):
            return
            
        base_getter = prop.__get__
        base_setter = prop.__set__
        
    def getter (self):
        if hasattr(self, '__nuclear_props'):
            properties = self.__nuclear_props
            if name in properties:
                return properties[name].get(
                   getter=functools.partial(base_getter, self)
                )

        return base_getter(self)

    def setter (self, value):
        if hasattr(self, '__nuclear_props'):
            properties = self.__nuclear_props
            if properties and name in properties:
                properties[name].set(
                    name,
                    value, 
                    getter=functools.partial(base_getter, self), 
                    setter=functools.partial(base_setter, self)
                )
                return
        base_setter(self, value)

    return property (getter, setter)    

def define_mutated_property(obj, key, desc):
    if key in ("__nuclear_props",):
        return
    
    # Patch, if necessary, the object's class property
    mutant_monkey_patch(obj, key)
    # Add the nuclear prop
    obj.__nuclear_props[key] =  desc

def has_mutated_prop(base_cls, prop_name):
    return hasattr(base_cls, '__nuclear_%s' % prop_name)

def flag_mutated_prop(base_cls, prop_name):
    setattr(base_cls, '__nuclear_%s' % prop_name, True)
    
def mutant_monkey_patch(obj, prop_name):
    if not hasattr(obj, "__nuclear_props"):
        obj.__nuclear_props = {}
    
    # We need to patch the core of the class
    base_cls = obj.__class__
    
    # Already been patched
    if has_mutated_prop(obj, prop_name):
        return
    
    if hasattr(base_cls, prop_name):
        prop = getattr(base_cls, prop_name)
        if type(prop) is types.FunctionType:
            prop = None
    else:
        prop = None
    
    setattr(base_cls, prop_name, mutant_patch_prop(prop, prop_name))
    flag_mutated_prop(base_cls, prop_name)
    
def assert_nuclear_mutant(obj):
    if not hasattr(obj, "__nuclear_props"):
        obj.__nuclear_props = {}     
        
##########################
# Make a list observable #
##########################
class ObservableList(list, object):
    def __init__(self, ls):
        for item in ls:
            self.append(item)
    
    def append(self, item):
        from .observe import observe
        item = mutate(item)
        observe(item)
        super().append(item)

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
        return result
    
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

UNPATCHABLE_TYPES = [
    str, int,
    types.FunctionType, functools.partial, types.MethodType, type,
    set, tuple,
] 
def mutate(value):
    """
        Patch the value to be observable
    """

    if any([isinstance(value, t) for t in UNPATCHABLE_TYPES]):
        return value
    
    if type(value) is list:
        obs_ls = ObservableList(value)
        assert_nuclear_mutant(obs_ls)
        list_monkey_patch(obs_ls)
        return obs_ls
    
    elif type(value) is dict:
        obs_dict = ObservableDict(value)
        assert_nuclear_mutant(obs_dict)
        dict_monkey_patch(obs_dict)
        return obs_dict
    else:
        assert_nuclear_mutant(value)
        return value  