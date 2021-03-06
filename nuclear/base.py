import functools 

from .reactivity import observe, Watcher, defineComputed, defineReactive
from .vdom.factory import create_vnode
from .vdom.vnode   import create_el, patch_el
from .log          import log

class BaseReactor:
    def __init__(self, id, template, data, computed, methods, watch, rods, globals, root, name=None):
        self._name = name if name else "_"
        self._id = id
        
        observe(self)
        
        self.data       = {}
        self.computed   = {}
        self.watchers   = []
        self.events     = {}
        self._globals   = {}
        
        self.bind_data(data)
        self.bind_globals(globals)    
        self.bind_computed(computed)
        self.bind_watch(watch)
        self.bind_methods(methods)
        
        self.w = Watcher(
            self, 
            lambda data: self.render(), 
            options={
                "flags": ["assembly_watcher"], 
                "name": str(self)
            }
        )
        
        self.template = template
        self.node = None

        self.rods = rods
        self.root = root

        self.created()
        self._destroyed = False
        self._mounted = False
    
    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
        
        if hasattr(self, "data") and key in self.data:
            log.assembly_data_props_changed(self, key, value)
        
        elif hasattr(self, "props") and key in self.props:
            log.assembly_data_props_changed(self, key, value)
            
    def get_name(self):
        return self._name
    
    def get_id(self):
        return self._id
    
    def render(self): 
        """
            Render the node
        """
        if self._destroyed:
            return
        
        if not self.root:
            return
            
        log.assembly_render(self)
        # Call the render function
        new_node = self.template(create_vnode, self)
        
        if self.node is None:
            self.node = new_node
            create_el(self.node, parent_el=self.root)

        else:
            self.node = patch_el(self.node, new_node)
        
        self.root.Layout()
        self.root.Refresh(eraseBackground=False)
        
        return self.node   
    
    def bind_methods(self, methods):
        for name, method in methods.items():
            setattr(self, name, functools.partial(method, self))        
    
    def bind_globals(self, globals):
        self._globals.update(globals)
        for k, v in globals.items():
            setattr(self, k, v)
    
    def bind_events(self, events):
        for ev_name, callback in events.items():
            if ev_name not in self.events:
                self.events[ev_name] =[] 
            self.events[ev_name].append(callback)
    
    def emit(self, event, args):
        log.assembly_event_emitted(self, event, args)
        
        if event in self.events:
            [c(args) for c in self.events[event]]
    
    def process_events(self):
        pass
    
    def bind_data(self, data):
        """
            Bind the dict of data to the reactor assembly/base
        """
        self.data.update(data)
        
        for k, v in data.items():
            defineReactive(self, k, v)
        
    def bind_computed(self, computed):
        """
            Bind the dict of computed data to the reactor assembly/base
        """
        self.computed.update(computed)
        
        for key, fn in computed.items():
            defineComputed(self, key, fn)
    
    def bind_watch(self, watch):
        """
            Create a watcher per data/computed so it can emit events if modified
        """
        for expr, cb in watch:
            self.watchers.append(
                Watcher(
                    self, 
                    expr, 
                    functools.partial(cb, self), 
                    options={"flags": ["assembly_watch"]}
                )
            )
    
    def mount(self):
        if self._mounted:
            return
        
        if self.w:
            self.w.run()

        for w in self.watchers:
            w.run()
        
        self._mounted = True
        self.mounted()
    
    def rod(self, key):
        """
            Return a rod based on its id within the reactor
        """
        if key in self.rods:
            return self.rods[key]
        else:
            return self.get_rod(key)

    # Lifecycle
    def get_rod(self, key):
        """
            If no rod was found, this method is called.
        """
        pass
        
    def created(self):
        pass
        
    def mounted(self):
        pass
    
    def destroyed(self):
        pass
    
    def patched(self):
        pass
    
    def els(self, key):
        n = self.node.get(key)
       
        if n:
            return n.get_el()
        else:
            return None
            
    def destroy(self):
        self._destroyed = True
        self.w.destroy()
        
        if self.node:
            self.node.destroy_el()
            self.node = None
            
        self.destroyed()
     
    def get_assembly_children(self):
        if self.node:
            return self.node.get_assembly_children()
        
        return []