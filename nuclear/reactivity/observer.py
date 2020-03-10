from .dep import Dep
from .react import defineReactive

class Observer:
    def __init__(self, value, restrain=None):
        self.value = value
        self.dep = Dep()
    
        if issubclass(type(value), list):
            self.observe_list(value)
        
        if hasattr(value, "__dict__"):
            self.walk(value, restrain)
        
        value.__ob__ = self

    def observe_list(self, ls):
        from .observe import observe
        
        for item in ls:
            observe(item)
    
    def walk(self, obj, restrain=None):
        attrs = {**obj.__dict__}
        
        if "__nuclear_props" in attrs:
            del attrs["__nuclear_props"]
        
        for key, value in attrs.items():  
            if restrain:
                if key in restrain:
                    defineReactive(obj, key, value)
            else:
                defineReactive(obj, key, value)