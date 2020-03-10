from .dep import Dep
from .watcher import Watcher

from .mutagen import mutate, define_mutated_property

class ComputedProperty:
    def __init__(self, obj, fn):
        self.fn = fn
        self.obj = obj
        
        self.dep = Dep()
        self.watcher = Watcher(obj, lambda d: self.compute(d))
        self.init = True
        
    def compute(self, data):
        self.value = self.fn(data)
        self.dep.notify()
    
    def get(self, getter):
        self.dep.depend()
        
        if self.init:
            self.watcher.get()
            self.init = False
        
        return self.value
     
    def set(self, new_value, getter, setter):
        raise Exception("Cannot modify a computed value.")
        
def defineComputed(obj, key, fn):     
    define_mutated_property(obj, key, ComputedProperty(obj, fn)) 
    
class ReactiveProperty:
    def __init__(self, value):
        from .observe import observe
        self.dep = Dep()
        self.ob_child = observe(value)
     
    def get(self, getter):
        self.dep.depend()
        
        if self.ob_child:
            self.ob_child.dep.depend()
        
        value = getter()
        return value
    
    def set(self, key, new_value, getter, setter):
        from .observe import observe        
        new_value = mutate(new_value)
        
        if hasattr(self, key) and id(getter()) == id(new_value):
            return

        setter(new_value)
        self.ob_child = observe(new_value)
        self.dep.notify()

def defineReactiveProperty(obj, key, value):
    # Mutate the value
    value = mutate(value)
    # Register a nuclear property
    define_mutated_property(obj, key, ReactiveProperty(value)) 
    # Set the value
    setattr(obj, key, value)
    
STACK = []
def defineReactive(obj, key, value):   
    mutate(obj)
    
    if key in obj.__nuclear_props:
        return
    
    if id(value) in STACK:
        return
    STACK.append(id(value))
    defineReactiveProperty(obj, key, value)
    STACK.pop(-1)