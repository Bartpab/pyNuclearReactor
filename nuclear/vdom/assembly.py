from .vnode import VNode
from ..log import log

def create_assembly_node(context, tag, props, events):
    from ..reactor import ReactorAssembly
    rod = context.rod(tag)
    
    rod_instance = rod()
    component = ReactorAssembly(**rod_instance, props=props, events=events, globals=context._globals, root=None, name=tag)
    
    log.create_assembly(component, props, events)
    return VNode.new_assembly(tag, component, props, [], events) 

def patch_assembly(current, new):
    log.assembly_patch(current, new)

    for k, v in new.props.items():
        setattr(current, k, getattr(new, k))
    
    for w in current.watchers:
        w.update()
        
    current.patched()