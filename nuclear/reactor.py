import functools

from .reactivity import observe, Watcher, defineComputed, defineReactive
from .vnode import create_wtree, create_element, patch, open_wtree, close_wtree

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

class Computed:
    def __init__(self, data, name, getter):
        self.w = Watcher(data, lambda data: self.update(data))
        self.name = name
        self.getter = getter
        self.w.get()
    
    def update(self, data):
        setattr(data, self.name, self.getter())
        
class BaseReactor:
    def __init__(self, template, data, computed, methods, rods, root):
        observe(self)
        
        self.bind_data(data)
        self.bind_computed(computed)
        
        self.w = Watcher(self, lambda data: self.render())
        
        self.template = template
        self.node = None
        
        for name, method in methods.items():
            setattr(self, name, functools.partial(method, self))
        
        self.events = []
        self.rods = rods
        self.root = root
    
    def patch(self):
        self.render()
    
    def render(self): 
        if not self.root:
            return
            
        tpl = self.template
        newNode = tpl(create_element, self)
        
        open_wtree(self.root)
        if self.node is None:
            self.node = newNode
            create_wtree(self.root, self.node)
        else:
            self.node = patch(self.node, newNode)
        
        close_wtree(self.root)

        return self.node   
    
    def emits(self, event_name, args):
        self.events.append((event_name, args))
        
    def bind_data(self, data):
        for k, v in data.items():
            defineReactive(self, k, v)
        
    def bind_computed(self, computed):
        for key, fn in computed.items():
            defineComputed(self, key, fn)

    def mount(self):
        self.w.get()
        self.mounted()
    
    # Lifecycle
    def mounted(self):
        pass

class ReactorAssembly(BaseReactor):
    def __init__(self, props, events, template, data, methods, computed, rods, root):
        BaseReactor.__init__(self, template, data, computed, methods, rods, root)
        
        self.events = {}
        
        self.bind_data(props)
        self.bind_events(events)
    
    def bind_events(self, events):
        for ev_name, callback in events:
            if ev_name not in self.events:
                self.events[ev_name] =[] 
            self.events[ev_name].append(callback)
    
    def emit(self, event, args):
        if event in self.events:
            [c(args) for c in self.events[event]]
        
class Reactor(BaseReactor):
    def set(self, key, value):
        value = objectify(value)
        setattr(self, key, value)

    def __init__(self, template, data, methods, computed, rods, root):
        BaseReactor.__init__(self, template, data, computed, methods, rods, root)

    def nexTick(self, dt):
        Watcher.run_all()


        