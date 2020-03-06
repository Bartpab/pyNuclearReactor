from .dep import Dep
from .react import defineReactive

from .augment import augment_list

class Observer:
    def __init__(self, value, restrain=None):
        from .observe import ObservableList
        self.value = value
        self.dep = Dep()

        if issubclass(type(value), list):
            augment_list(value)
            self.observe_list(value)
        else:
            self.walk(value, restrain)
        
        value.__ob__ = self
    
    def observe_list(self, ls):
        from .observe import observe
        for item in ls:
            observe(item)

    def walk(self, obj, restrain=None):
        attrs = {**obj.__dict__}

        for key, value in attrs.items():   
            if restrain:
                if key in restrain:
                    defineReactive(obj, key, value)
            else:
                defineReactive(obj, key, value)