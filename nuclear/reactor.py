import functools

from .reactivity import observe, Watcher, defineComputed, defineReactive

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

class Computed:
    def __init__(self, data, name, getter):
        self.w = Watcher(data, lambda data: self.update(data))
        self.name = name
        self.getter = getter
        self.w.get()
    
    def update(self, data):
        setattr(data, self.name, self.getter())
        
from copy import copy

class BaseReactor:
    def __init__(self, template, data, computed, methods, rods, globals, root):
        observe(self)
        self.data = {}
        
        self.bind_data(data)
        self.bind_data(globals)
        self.bind_computed(computed)
        
        self.globals = globals
        
        self.w = Watcher(self, lambda data: self.render())
        
        self.template = template
        self.node = None
        
        for name, method in methods.items():
            setattr(self, name, functools.partial(method, self))
            
        self.events = []
        self.rods = rods
        self.root = root
        
        self.created()
        
        self._destroyed = False
    def patch(self):
        self.render()
    
    def render(self): 
        """
            Render the node
        """
        if self._destroyed:
            return
        
        if not self.root:
            raise Exception("Cannot render without root element")
            
        tpl         = self.template
        
        # Call the render function
        new_node    = tpl(create_vnode, self)
        
        if self.node is None:
            self.node           = new_node
            create_el(self.node, parent_el=self.root)
        else:
            self.node = patch(self.node, new_node)
        
        self.root.Layout()
        
        return self.node   
    
    def emits(self, event_name, args):
        self.events.append((event_name, args))
        
    def bind_data(self, data):
        self.data.update(data)
        for k, v in data.items():
            defineReactive(self, k, v)
        
    def bind_computed(self, computed):
        for key, fn in computed.items():
            defineComputed(self, key, fn)

    def mount(self):
        self.w.get()
        self.mounted()
    
    def rod(self, key):
        if key in self.rods:
            return self.rods[key]
        else:
            return self.get_rod(key)

    # Lifecycle
    def get_rod(self, key):
        pass
        
    def created(self):
        pass
        
    def mounted(self):
        pass
    
    def destroyed(self):
        pass
    
    def destroy(self):
        self._destroyed = True
        self.w.destroy()
        if self.node:
            self.node.destroy_el()
            self.node = None
        
        self.destroyed()
        
class ReactorAssembly(BaseReactor):
    def __init__(self, props, events, template, data, methods, computed, rods, globals, root, name):
        data_and_props = {**data}
        data_and_props.update(props)
        self.name = name
        BaseReactor.__init__(self, template, data_and_props, computed, methods, rods, globals, root)
        self.events = {}
        self.bind_events(events)
    
    def bind_events(self, events):
        for ev_name, callback in events.items():
            if ev_name not in self.events:
                self.events[ev_name] =[] 
            self.events[ev_name].append(callback)
    
    def emit(self, event, args):
        if event in self.events:
            [c(args) for c in self.events[event]]
    
    def __str__(self):
        return "ReactorAssembly::{}".format(self.name)
        
class Reactor(BaseReactor):
    def set(self, key, value):
        value = objectify(value)
        setattr(self, key, value)

    def __init__(self, template, data, methods, computed, rods, root, globals=None):
        if not globals:
            globals = {}
            
        BaseReactor.__init__(self, template, data, computed, methods, rods, globals, root)

    def nexTick(self, dt):
        Watcher.run_all()


        