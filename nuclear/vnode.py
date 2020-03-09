import wx
import functools

from .widgets import Tree

def helpers(h, self):
    def _h(tag, data, children, events=None):
        return h(self, tag, data, children, events)    
    
    def _it(iterator, el_fn):
        return [el_fn(el) for el in iterator]
    
    def _if(b, if_fn, else_fn=None):
        if b:
            return if_fn()
        elif else_fn:
            return else_fn()
        
        return []
    
    def _f(fn):
        return functools.partial(fn, self)
    
    return _h, _it, _if, _f

def set_el_data(el, data):
    for key, value in data.items():
        if key in ("sopt", "key"):
            continue
        
        wMethName = "Set" + key[0].upper() + key[1:]
        wMeth = getattr(el, wMethName)
        wMeth(value)
        
def unbind_el_events(el, events):
    return
    for k, v in events.items():
        el.Unbind(k, v)    
        
def bind_el_events(el, events):
    for k, v in events.items():
        if k == "click" and type(el) is wx.Button:
            el.Bind(wx.EVT_BUTTON, v)
        elif k == "change" and type(el) is wx.TextCtrl:
            el.Bind(wx.EVT_TEXT, lambda e: v(e.GetEventObject().GetValue()))
        else:
            el.Bind(k, v)

def create_wel(parent_el, el_factory, data, events):
    """
        Create a widget node
    """
    el = el_factory(parent=parent_el)
    set_el_data(el, data)
    bind_el_events(el, events)
    return el

###################
# WTree Rendering #
###################
SIZER_STACK = []
PARENT_STACK = []

def open_wtree(root_el):
    if root_el.GetSizer():
        SIZER_STACK.append(root_el.GetSizer())

def close_wtree(root_el):
    if root_el.GetSizer():
        SIZER_STACK.remove(root_el.GetSizer())
    
def create_wtree(parent_el, vnode):
    """
        Recursively create the widget tree
    """
    if vnode.is_component:
        vnode.component_instance.root = parent_el
        vnode.component_instance.mount()
        parent_el.Layout()
    
    else:
        el = create_wel(parent_el, vnode.el_factory, vnode.data, vnode.events)
        vnode.el = el
        
        pop = False

        if SIZER_STACK:
            kw = vnode.data["sopt"] if "sopt" in vnode.data else {}
            SIZER_STACK[-1].Add(el, **kw)
        
        if el.GetSizer():
            pop = True
            SIZER_STACK.append(el.GetSizer())
        
        for cvnode in vnode.children:
            create_wtree(el, cvnode)
        
        el.Layout()
        
        if pop:
            SIZER_STACK.pop(-1)
    
def to_camel_case(snake_str):
    components = snake_str.split('-')
    return components[0].title() + ''.join(x.title() for x in components[1:])

def is_native_element(tag):
    cTag = to_camel_case(tag)
    return cTag in dir(wx) 
    
def create_native_element(tag, data, children, events=None):
    cTag = to_camel_case(tag)

    if is_native_element(tag):
        return VNode(tag, getattr(wx, cTag), data, children, events)
    else:       
        raise Exception(cTag)
 
def create_assembly(context, tag, props, events):
    from .reactor import ReactorAssembly
    rod = context.rod(tag)
    component = ReactorAssembly(**rod(), props=props, events=events, globals=context.globals, root=None)
    node = VNode(tag, None, props, [], events) 
    node.component_instance = component
    node.is_component = True
    return node
  
def create_element(context, tag, data, children, events=None):
    if is_native_element(tag):
        node = create_native_element(tag, data, children, events)
    elif tag == "tree":
        return VNode(tag, Tree, data, children, events) 
    else:
        node = create_assembly(context, tag, data, events)
    return node

def same_vnode(old, vnode):
    same_tag  = old.tag == vnode.tag
    same_id  = old.id == vnode.id
    
    return same_tag and same_id

def update_children(parent_el, old_ch, new_ch):
    to_remove = []
    to_patch = []
    
    n_list = new_ch[:]
    
    for o in old_ch:
        f = None
        for n in n_list:
            if same_vnode(o, n):
                f = n
                break
                
        if f is None:
            to_remove.append(o)
        else:
            to_patch.append((o, f))
            n_list.remove(f)
    
    # What's left is new
    to_add = n_list[:]

    for to_r in to_remove:
        to_r.destroy()
    
    for to_a in to_add:
        create_wtree(parent_el, to_a)
    
    for o, v in to_patch:
        patch(o, v)
  
def patch_vnode(old, vnode):
    if old == vnode:
        return
    
    if old.is_component:
        old.component_instance.patch()
    
    else:
        el = old.el
        vnode.el = el

        unbind_el_events(el, old.events)
        
        # We don't patch the sizer
        if "sizer" in vnode.data:
            del vnode.data["sizer"]
            
        set_el_data(el, vnode.data)
        bind_el_events(el, vnode.events)
        
        old_ch = old.children
        new_ch = vnode.children
        
        pop = False
        
        if el.GetSizer():
            pop = True
            SIZER_STACK.append(el.GetSizer())
            
        update_children(el, old_ch, new_ch)
        
        if pop:
            SIZER_STACK.pop(-1)
        
def patch(old, vnode):
    """ 
        Check if vnode needs to be patched by comparing it to the new version
    """
    # The component is similar, we need to transfer the old node to the new without breaking the node chain
    if same_vnode(old, vnode):
        patch_vnode(old, vnode)
    
    # The component change drastically, we need to swap it and destory the old one
    elif old.is_component:
        p_el = old.get_parent_el()
        old.destroy()  
        create_wtree(p_el, vnode)
    
    # A wx node has changed, we need to swap it and destory the old one
    else:
        p_el = old.get_parent_el()
        old.destroy() 
        create_wtree(p_el, vnode)
    
    for el in vnode.get_els():
        el.Layout()

    return vnode
        
class VNode:
    def __init__(self, tag, el_factory_or_assembly, data, children, events=None):        
        self.tag = tag
        self.el = None
        self.component_instance = None

        self.el_factory = el_factory_or_assembly
        self.is_component = False

        self.events = {} if events is None else {**events}
        self.data = {**data}
        
        self.parent = None
        self.children = []
        self.set_children(children)
        
        self.key = data["key"] if "key" in data else None
        self.id = 1
    
    def get_els(self):
        s = [self]
        els = []
        
        while len(s):
            e = s.pop(0)
            if e.is_component:
                s.append(e.component_instance.node)
            else:
                els.append(e.el)
        return els
    
    def get_parent_el(self):
        if self.is_component:
            return self.component_instance.root
        else:
            return self.el.GetParent()
    
    def destroy(self):
        self.destroy_els()
    
    def destroy_els(self):
        for el in self.get_els():
            if el:
                el.Destroy()
    
    def get(self, key):
        s = [self]
        
        while len(s):
            e = s.pop(0)
            if e.key == key:
                return e
            s.extend(e.children)
    
    def set_children(self, children):
        self.children = []
        for child in children:
            child.parent = self
            self.children.append(child)
            child.id = len(self.children)