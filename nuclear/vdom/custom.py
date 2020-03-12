import wx
from .vnode import VNode
from ..widgets import ComboBox, Tree, create_menu_bar, create_menu, create_menu_item

def to_camel_case(snake_str):
    components = snake_str.split('-')
    return components[0].title() + ''.join(x.title() for x in components[1:])

def is_custom_element(tag):
    cTag = to_camel_case(tag)
    return cTag in ["ComboBox", "Tree", "MenuBar", "Menu", "MenuItem"]
    
def create_custom_node(tag, data, children, events=None):
    cTag = to_camel_case(tag)

    if cTag == "Tree":
        return VNode.new_native(tag, Tree, data, children, events)
    elif cTag == "ComboBox":
        return VNode.new_native(tag, ComboBox, data, children, events)
    elif cTag == "MenuBar":
        return VNode.new_native(tag, create_menu_bar, data, children, events)
    
    elif cTag == "Menu":
        return VNode.new_native(tag, create_menu, data, children, events)
    
    elif cTag == "MenuItem":
        return VNode.new_native(tag, create_menu_item, data, children, events)
        
    else:       
        raise Exception(cTag)