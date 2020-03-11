from .reactivity import observe, defineComputed, defineReactive
import functools

class State:
    def __init__(self):
        self.actions = {}
        observe(self)

    def define(self, key, value):
        defineReactive(self, key, value)

    def define_getter(self, key, fn):
        defineComputed(self, key, fn)      
    
    def define_action(self, key, fn):
        self.actions[key] = fn
    
    def get(self, key):
        return getattr(self, key)
    
    def map_getter(self, dest, key, dest_name=None):
        if not dest_name:
            dest_name = key
        
        defineComputed(dest, dest_name, lambda dest: self.get(key))
    
    def map_action(self, dest, key, dest_name=None):
        if not dest_name:
            dest_name = key
            
        def __action__(*args, **kwargs):
            return self.dispatch(key, *args, **kwargs)
        
        setattr(dest, dest_name, __action__)
    
    def dispatch(self, key, *args, **kwargs):
        return self.actions[key](self, *args, **kwargs)