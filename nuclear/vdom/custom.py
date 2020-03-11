import wx
from .vnode import VNode
from ..widgets import Tree

def to_camel_case(snake_str):
    components = snake_str.split('-')
    return components[0].title() + ''.join(x.title() for x in components[1:])

def is_custom_element(tag):
    cTag = to_camel_case(tag)
    return cTag in ["Tree"]
    
def create_custom_node(tag, data, children, events=None):
    cTag = to_camel_case(tag)

    if cTag == "Tree":
        return VNode.new_native(tag, Tree, data, children, events)
    else:       
        raise Exception(cTag)