from .dep import Dep

def reactifyObject(obj):
    if hasattr(obj, '__accessors'):
        return
    
    setattr(obj, '__accessors', {})
    setattr(obj, '__data', {})

def defineComputed(obj, key, fn):
    from .observe import observe
    from .augment import augment    
    
    obj.__data[key] = {
        "dep": Dep(),
        "w": Watcher(obj, __compute__)
    }
    
    def __compute__(d):
        obj.__data[key]["val"] = fn(d)
    
    def __getter__(self):
        if "val" not in obj__data[key]:
            obj__data[key]["w"].get()
        
        return obj.__data[key]["val"] 
    
    def __setter__(self, newValue): 
        pass
    
    obj.__accessors[key] = (__getter__, __setter__)
    
def defineReactiveProperty(obj, key, value):
    from .observe import observe
    from .augment import augment
    
    value = augment(value)
    
    obj.__data[key] = {
        "dep": Dep(),
        "ob_child": observe(value),
        "val": value
    }
    
    def __getter__(self):
        self.__data[key]['dep'].depend()
        if "ob_child" in self.__data[key] and self.__data[key]['ob_child']:
            self.__data[key]['ob_child'].dep.depend()
        
        return self.__data[key]['val']
    
    def __setter__(self, newValue): 
        newValue = augment(newValue)
        
        if self.__data[key]['val'] == newValue:
            return
            
        self.__data[key]['val'] = newValue
        self.__data[key]['ob_child'] = observe(newValue)
        
        self.__data[key]['dep'].notify()
    
    obj.__accessors[key] = (__getter__, __setter__) 

def defineReactive(obj, key, value):   
    reactifyObject(obj)
    
    if key in obj.__accessors:
        return
    
    defineReactiveProperty(obj, key, value)