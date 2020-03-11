import types
import functools
from inspect import getfullargspec

_monkey_patch_index = 0
_not_set            = object ()

def is_property(prop):
    if not hasattr(prop, '__get__'):
        return False

    if not hasattr(prop, '__set__'):
        return False
    
    return True

class MutantProperty:
    def __init__(self, prop, name):
        self.prop = prop
        self.name = name
    
    def __get__(self, obj, objtype=None): 
        name = self.name
        prop = self.prop
        
        if prop is None:
            def fbase_getter(self, obj):
                return self.value
            
            base_getter = functools.partial(fbase_getter, self, obj)
        
        else:
            base_getter = functools.partial(prop.__get__, obj, objtype)
                                
        if hasattr(obj, '__nuclear_props'):
            properties = getattr(obj, "__nuclear_props")
            if name in properties:
                return properties[name].get(
                   getter=base_getter
                )
        
        return base_getter()
        
    def __set__(self, obj, value):
        name = self.name
        prop = self.prop
        
        if prop is None:
            def fbase_getter(self, obj):
                return self.value 
            
            def fbase_setter(self, obj, value):
                self.value = value
            
            base_getter = functools.partial(fbase_getter, self, obj)
            base_setter = functools.partial(fbase_setter, self, obj)
        else:
            base_getter = functools.partial(prop.__get__, obj, None)
            base_setter = functools.partial(prop.__set__, obj)
        
        if hasattr(obj, '__nuclear_props'):
            properties = getattr(obj, "__nuclear_props")
            if properties and name in properties:
                properties[name].set(
                    name,
                    value, 
                    getter=base_getter, 
                    setter=base_setter
                )
                return
        
        base_setter(value) 
        
def mutant_patch_prop(prop, name):
       return MutantProperty (prop, name)    

def define_mutated_property(obj, key, desc):
    if key in ("__nuclear_props",):
        return
    
    # Patch, if necessary, the object's class property
    if mutant_monkey_patch(obj, key):
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
        return True
    
    prop = None
    
    if hasattr(base_cls, prop_name):
        prop = getattr(base_cls, prop_name)
        if not is_property(prop):
            return False      
    else:
        prop = None
        
    setattr(base_cls, prop_name, mutant_patch_prop(prop, prop_name))
    flag_mutated_prop(base_cls, prop_name)
    return True
    
def assert_nuclear_mutant(obj):
    if not hasattr(obj, "__nuclear_props"):
        obj.__nuclear_props = {}     
        
##########################
# Make a list observable #
##########################
class ObservableList(list):
    def __init__(self, ls):
        for item in ls:
            self.append(item)
    
    def append(self, item):
        from .observe import observe
        item = mutate(item)
        observe(item)
        super().append(item)

class ObservableDict(dict):
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
        return value # Cannot patch yet
        obs_dict = ObservableDict(value)
        assert_nuclear_mutant(obs_dict)
        dict_monkey_patch(obs_dict)
        return obs_dict
    else:
        try:
            assert_nuclear_mutant(value)
        finally:
            return value  