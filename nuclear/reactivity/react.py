from .dep import Dep
from .watcher import Watcher

from .patch import reactify

class ComputedProperty:
    def __init__(self, obj, fn):
        self.fn = fn
        self.obj = obj
        
        self.dep = Dep()
        self.w = Watcher(obj, self.compute)
        self.init = True
        
    def compute(self, data):
        self.value = self.fn(data)
        self.dep.notify()
    
    def get(self):
        self.dep.depend()
        
        if self.init:
            self.w.get()
            self.init = False
        
        return self.value
     
    def set(self):
        raise Exception("Cannot modify a computed value.")
        
def defineComputed(obj, key, fn):      
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
    
    def set(self, new_value, getter, setter):
        from .observe import observe        
        new_value = reactify(new_value)
        
        try:        
            if getter() == new_value:
                return
        except:
            pass
        
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