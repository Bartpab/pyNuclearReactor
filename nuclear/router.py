from .base import BaseReactor

from .vdom.factory import create_vnode
from .vdom.vnode   import create_el, patch_el

class RouterAssembly(BaseReactor):
    def __init__(self, router, props, events, globals, root, name):
        BaseReactor.__init__(self, 
            template=None, 
            data={}, 
            computed={}, 
            methods={}, 
            watch={}, 
            rods={}, 
            globals=globals, 
            root=root
        )
        
        self.props = {}
        self.router = router
        self.router.sub(self)
      
    def patch(self):
        self.render()
        
    def destroyed(self):
        self.router.unsub(self)
    
    def update(self):
        self.render()
    
    def render(self): 
        """
            Render the node
        """   
        if self._destroyed:
            return
            
        if not self.root:
            return

        # Call the render function
        new_node = create_vnode(
            self,
            self.router.get_current_route(),
            self.router.get_current_route_args(), 
            [],
            {}
        )
        
        if self.node is None:
            self.node = new_node
            create_el(self.node, parent_el=self.root)
        
        else:
            self.node = patch_el(self.node, new_node)
        
        self.root.Layout()
        return self.node   
    
    def get_rod(self, key):
        return self.router.get_current_rod()
    
    def next_tick(self, dt):
        self.process_events()
        
        for c in self.get_assembly_children():
            c.next_tick(dt) 
            
class Router:
    def __init__(self):
        self._routes = {}
        self.url = "default"
        self.args = {}
        self._subs = []
    
    def notify(self):
        for sub in self._subs:
            sub.update()
    
    def sub(self, sub):
        if sub not in self._subs:
            self._subs.append(sub)
    
    def unsub(self, sub):
        if sub in self._subs:
            self._subs.remove(sub)
    
    def go_to(self, url, **kw):
        self.url = url
        self.args = kw
        self.notify()
    
    def define(self, route, rod):
        self._routes[route] = rod
    
    def get_current_route(self):
        return self.url
    
    def get_current_rod(self):
        return self._routes[self.url]
    
    def get_current_route_args(self):
        return self.args
    