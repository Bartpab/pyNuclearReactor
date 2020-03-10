from .dep import Dep
from .react import defineReactive
import inspect
import sqlalchemy

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
        for key, value in inspect.getmembers(obj):  
            if (key.startswith("__") and key.endswith("__")) or key in ("__nuclear_props",):
                continue
            try:
                if restrain:
                    if key in restrain:
                        defineReactive(obj, key, value)
                else:
                    defineReactive(obj, key, value)
            except Exception as e:
                pass