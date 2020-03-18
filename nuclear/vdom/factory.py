from .native    import is_native_element, create_native_node
from .assembly  import create_assembly_node 
from .custom    import is_custom_element, create_custom_node

from .vnode     import VNode
from .router    import create_router_node

def create_vnode(context, tag, data, children, events=None):
    vnode = None

    if is_custom_element(tag):
        vnode = create_custom_node(tag, data, children, events)
    
    elif is_native_element(tag):
        vnode = create_native_node(tag, data, children, events)
    
    elif tag == "router":
        vnode = create_router_node(context, tag, data, events)
    
    else:
        vnode = create_assembly_node(context, tag, data, events)
    
    return vnode