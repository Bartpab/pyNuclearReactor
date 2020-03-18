from .vnode import VNode

def create_router_node(context, tag, props, events):
    from ..router import RouterAssembly
    
    router_assembly = RouterAssembly(
        context._globals["g_router"], 
        props=props, 
        events=events, 
        globals=context._globals, 
        root=None, 
        name=tag
    )
    
    return VNode.new_assembly(tag, router_assembly, props, [], events) 
