from .native    import is_native_element, create_native_node
from .assembly  import create_assembly_node 
from .custom    import is_custom_element, create_custom_node

from .vnode     import VNode
  
def create_vnode(context, tag, data, children, events=None):
    if is_native_element(tag):
        return create_native_node(tag, data, children, events)
    elif is_custom_element(tag):
        return create_custom_node(tag, data, children, events)
    else:
        return create_assembly_node(context, tag, data, events)