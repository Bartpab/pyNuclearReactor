import functools

from .base       import BaseReactor
from .reactivity import observe, Watcher, defineComputed, defineReactive

from .style        import StyleEngine
from .vdom.factory import create_vnode
from .vdom.vnode   import create_el, patch

def dict2obj(**kw):
    obj = type("DataEntry", (), {})() 
    
    for k, v in kw.items():
        setattr(obj, k, v)
    
    return obj

def objectify(o):
    if type(o) is dict:
        for k, v in o.items():
            o[k] = objectify(v)
    
        return dict2obj(**o)
    
    return o

from copy import copy

class ReactorAssembly(BaseReactor):
    def __init__(self, props, events, template, data, methods, computed, watch, rods, globals, root, name):
        self.props = {**props}
        self.data = {**data}

        data_and_props = {**data}
        data_and_props.update(props)
        self.name = name

        BaseReactor.__init__(self, 
            template=template, 
            data=data_and_props, 
            computed=computed, 
            methods=methods, 
            watch=watch, 
            rods=rods, 
            globals=globals, 
            root=root,
            name=name
        )
        
        self.events = {}
        self.bind_events(events)
    
    def __str__(self):
        return "ReactorAssembly::{}".format(self.name)
    
    def next_tick(self, dt):
        self.process_events()
        
        for c in self.get_assembly_children():
            c.next_tick(dt)       
            
class Reactor(BaseReactor):
    def set(self, key, value):
        value = objectify(value)
        setattr(self, key, value)

    def __init__(self, template, data, methods, computed, watch, rods, root, globals=None):
        if not globals:
            globals = {}

        BaseReactor.__init__(self, 
            template=template, 
            data=data, 
            computed=computed, 
            methods=methods, 
            watch=watch, 
            rods=rods, 
            globals=globals, 
            root=root)

    def next_tick(self, dt):
        Watcher.run_all()
        StyleEngine.run_all()
        self.process_events()
        
        for c in self.get_assembly_children():
            c.next_tick(dt)
        
        


        