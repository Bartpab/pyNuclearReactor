from .native import set_data_to_native, set_events_to_native, set_nesting_properties, set_style_to_native
from .el_helpers import entering_el, leaving_el
from .children_helpers import update_children
from ..style import StyleEngine

class VNode:
    @staticmethod
    def new_native(tag, el_factory, data, children, events):
        return NativeVNode(tag, el_factory, data, children, events)
    
    @staticmethod
    def new_assembly(tag, component_instance, data, children, events):
        return AssemblyVNode(tag, component_instance, data, children, events)
    
    def __init__(self, tag, data, children, events):
        self.parent     = None
        self.parent_el  = None
        self.tag = tag
        self.data = data
        self.set_children(children)
        self.events = events
        self.id = None
        self.key = None if "key" not in data else data["key"]
    
    def get(self, key):
        s = [self]
        
        while s:
            e = s.pop()
            if e.key == key:
                return e
            else:
                s.extend(e.children)
        
        return None
    
    def set_parent(self, p):
        p.add_child(self)
    
    def set_children(self, children):
        self.children = []
        for c in children:
            self.add_child(c)
    
    def add_child(self, child):
        child.parent = self
        child.id = len(self.children)
        self.children.append(child)
    
    def remove_child(self, child):
        self.children.remove(child)
            
    def get_el(self):
        raise NotImplementedError()
    
    def create_el(self, el_contexts):
        raise NotImplementedError()
    
    def patch_from(self, other, el_contexts):
        raise NotImplementedError()
    
    def get_parent_el(self, raise_if_none=False):
        p_el = self.parent.get_el() if self.parent else self.parent_el
        
        if not p_el and raise_if_none:
            raise Exception("No parent element is available")
        
        return p_el
       
    def transfer(self, other):
        if self.parent:
            other.parent = self.parent
        else:
            other.parent_el = self.parent_el
    
    def same(self, other):
        same_tag  = self.tag == other.tag
        same_id  = self.id == other.id        
        return same_tag and same_id
    
    def destroy(self):
        if self.parent:
            self.parent.remove_child(self)
        self.destroy_el()
    
    def destroy_el(self):
        raise NotImplementedError()
        
class AssemblyVNode(VNode):
    def __init__(self, tag, component_instance, data, children, events):
        VNode.__init__(self, tag, data, children, events)
        self.component_instance = component_instance
    
    def create_el(self, el_contexts):
        self.component_instance.root = self.get_parent_el()
        self.component_instance.mount()
    
    def patch_from(self, other, el_contexts, recreate): 
        if recreate:
            self.component_instance.destroy()
            self.component_instance = other.component_instance
            self.component_instance.root = self.get_parent_el()
            self.component_instance.mount()       
        else:
            self.component_instance.patch()
            
    def get_el(self):
        return self.parent_el
    
    def destroy_el(self):
        if self.component_instance:
            self.component_instance.destroy()

class NativeVNode(VNode):
    def __init__(self, tag, el_factory, data, children, events):
        VNode.__init__(self, tag, data, children, events)
        self.el_factory = el_factory
    
    def get_el(self):
        return self.el
    
    def destroy_el(self):
        if self.el:
            StyleEngine.remove(self.el)
            self.el.Destroy()
        
    def create_el(self, el_contexts):
        try:
            self.el = self.el_factory(
                parent=self.get_parent_el(raise_if_none=True)
            )
        except Exception as e:
            raise Exception("Cannot create el from vnode {}, because {} <Stack={}>.".format(self.tag, str(e), el_contexts["stack"]))
        
        try:
            set_nesting_properties(self.data, self.el, el_contexts)
            set_style_to_native(self.el, StyleEngine)
            set_data_to_native(self.el, self.data)
            set_events_to_native(self.el, self.events)
            StyleEngine.apply(self.el)

        except Exception as e:
            print(e)
        
        entering_el(self.el, el_contexts) # Entering node
        
        for c in self.children:
            c.create_el(el_contexts)
        
        leaving_el(self.el, el_contexts) # Leaving node
        
        
    def patch_from(self, other, el_contexts, recreate = False):
        self.data   = {**other.data}
        self.events = {**other.events}
        
        if recreate:
            self.destroy_el()
            self.el_factory = other.el_factory
            self.create_el(el_contexts)
        else:
            set_nesting_properties(self.data, self.el, el_contexts)
            set_data_to_native(self.el, self.data)
            set_events_to_native(self.el, self.events)  
            
            entering_el(self.el, el_contexts) # Entering node
            update_children(self, other, el_contexts)
            leaving_el(self.el, el_contexts) # Leaving node
        
def create_el_contexts(vnode):
    p_el = vnode.get_parent_el()
    
    c = {
        "sizers": [],
        "stack": []
    }
    
    if p_el.GetSizer():
        c["sizers"].append(p_el.GetSizer())
    
    return c
    
def create_el(vnode, parent_el = None, el_contexts = None):
    if not parent_el and not vnode.parent:
        raise Exception("Cannot create element as no root was defined (either virtual or real ones)")
    
    if not vnode.parent:
        vnode.parent_el = parent_el
    
    if not el_contexts:
        el_contexts = create_el_contexts(vnode)
    
    return vnode.create_el(el_contexts)

def patch(old, new, el_contexts=None, order_changed=False):
    """
        Patch the vnode and apply it to the real one
    """
    if not el_contexts:
        el_contexts = create_el_contexts(old)

    if old.same(new):
        old.patch_from(new, el_contexts, order_changed)
        return old
    else:   
        old.transfer(new)
        old.destroy_el()
        new.create_el(el_contexts)
        return new
