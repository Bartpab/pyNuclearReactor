from .vnode import VNode

def create_assembly_node(context, tag, props, events):
    from ..reactor import ReactorAssembly
    rod = context.rod(tag)
    
    rod_instance = rod()
    component = ReactorAssembly(**rod_instance, props=props, events=events, globals=context._globals, root=None, name=tag)
    return VNode.new_assembly(tag, component, props, [], events) 