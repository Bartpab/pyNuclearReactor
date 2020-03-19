from .dep import Dep
from .react import defineReactive
import inspect
import sqlalchemy
import types

class Observer:
    def __init__(self, value, restrain=None):
        self.value = value
        self.dep = Dep(src=value)
    
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
        attrs = {**obj.__dict__}.items()
        # attrs = inspect.getmembers(obj)
        for key, value in attrs:  
            if type(value) in (types.FunctionType, types.MethodType):
                continue
            if key.startswith("_"):
                continue
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