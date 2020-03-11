from .vnode import VNode

def create_assembly_node(context, tag, props, events):
    from ..reactor import ReactorAssembly
    rod = context.rod(tag)
    component = ReactorAssembly(**rod(), props=props, events=events, globals=context.globals, root=None)
    return VNode.new_assembly(tag, component, props, [], events) 