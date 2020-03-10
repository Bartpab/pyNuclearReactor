from .dep import Dep
from .watcher import Watcher

from .patch import reactify

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
    reactify(obj)
    obj.__nuclear_props[key] = ComputedProperty(obj, fn)
    
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
        new_value = reactify(new_value)

        setter(new_value)
        self.ob_child = observe(new_value)
        self.dep.notify()

def defineReactiveProperty(obj, key, value):
    value = reactify(value)
    obj.__nuclear_props[key] = ReactiveProperty(value) 
    setattr(obj, key, value)
    
STACK = []
def defineReactive(obj, key, value):   
    if key == "__nuclear_props":
        return
    
    reactify(obj)
    
    if key in obj.__nuclear_props:
        return
    
    if id(value) in STACK:
        return
    
    STACK.append(id(value))
    defineReactiveProperty(obj, key, value)
    STACK.pop(-1)