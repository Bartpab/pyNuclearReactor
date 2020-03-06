import wx
import functools

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

class Tree(wx.TreeCtrl):
    @staticmethod
    def default_walker(self, node):
        if not hasattr(node, "items"):
            return []
        
        items = []
        
        for key, value in node.items():
            if not hasattr(value, "items"):
                items.append((key, value, False))
            else:
                items.append((key, value, True))
        
        return items
        
    def __init__(self, parent, id, pos, size, style):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)    
    
    def SetWalker(self, walker):
        self.walker = walker
    
    def rec_tree(self, node, tree_node=None):
        for key, value, is_node in self.walker(tree): 
            if tree_node is None:
                if not is_node:
                    ctree_node = self.AddRoot(key + ": " +value)
                else:
                    ctree_node = self.AddRoot(key)
                    self.rec_tree(value, ctree_node)
            else:
                if not is_node:
                    ctree_node = self.AppendItem(tree_node, key)
                    self.rec_tree(value, ctree_node)
                else:
                    self.SetPyData(tree_node, (key, value))
                    
    def SetTree(self, tree):
        self.rec_tree(tree)

def set_el_data(el, data):
    for key, value in data.items():
        if key in ("sopt",):
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
        vnode.componentInstance.root = parent_el
        vnode.mount()
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
        if cTag == "Tree":
            return VNode(tag, Tree, data, children, events) 
        
        raise Exception(cTag)
 
def create_assembly(context, tag, props, events):
    from .reactor import ReactorAssembly
    rod = context.rods[tag]
    
    component = ReactorComponent(**rod(), props=props, events=events, root=None)
    component.bind(events)
    
    return VNode(tag, component, data, children, events) 
  
def create_element(context, tag, data, children, events=None):
    if is_native_element(tag):
        node = create_native_element(tag, data, children, events)
    else:
        node = create_assembly(context, tag, data, children, events)
    
    return node

def same_vnode(old, vnode):
    same_tag  = old.tag == vnode.tag
    same_key  = old.key == vnode.key
    
    return same_tag and same_key

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
        to_r.el.Destroy()
    
    for to_a in to_add:
        create_wtree(parent_el, to_a)
    
    for o, v in to_patch:
        patch(o, v)
        
def patch_vnode(old, vnode):
    if old == vnode:
        return
    
    if old.is_component:
        old.componentInstance.patch()
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
    if same_vnode(old, vnode):
        patch_vnode(old, vnode)
    
    else:
        o_el = old.el
        p_el = o_el.GetParent()
        o_el.Destroy()   
        create_wtree(p_el, vnode)
    
    vnode.el.Layout()
    
    return vnode
        
class VNode:
    def __init__(self, tag, el_or_component_factory, data, children, events=None):        
        self.tag = tag
        self.el = None
        self.componentInstance = None
        
        if type(el_or_component_factory) is dict: 
            self.component_factory = el_or_component_factory
            self.is_component = True
        else:
            self.el_factory = el_or_component_factory
            self.is_component = False

        self.events = {} if events is None else {**events}
        self.data = {**data}
        
        self.parent = None
        self.children = []
        self.set_children(children)
        
        self.key = data[key] if "key" in data else None
        
    def set_children(self, children):
        self.children = []
        for child in children:
            child.parent = self
            self.children.append(child)
            child.key = len(self.children)