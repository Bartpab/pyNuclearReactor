import wx

def to_camel_case(snake_str):
    components = snake_str.split('-')
    return components[0].title() + ''.join(x.title() for x in components[1:])

def is_native_element(tag):
    cTag = to_camel_case(tag)
    return cTag in dir(wx) 
    
def create_native_node(tag, data, children, events=None):
    from .vnode import VNode
    cTag = to_camel_case(tag)

    if is_native_element(tag):
        return VNode.new_native(tag, getattr(wx, cTag), data, children, events)
    else:       
        raise Exception(cTag)

def set_data_to_native(el, data):
    for key, value in data.items():
        if key in ("sopt", "key"):
            continue

        wMethName = "Set" + key[0].upper() + key[1:]
        wMeth = getattr(el, wMethName)
        wMeth(value)


def set_events_to_native(el, events):
    for k, v in events.items():
        if k == "click" and type(el) is wx.Button:
            el.Bind(wx.EVT_BUTTON, v)
        elif k == "change" and type(el) is wx.TextCtrl:
            el.Bind(wx.EVT_TEXT, lambda e: v(e.GetEventObject().GetValue()))
        elif k == "change" and isinstance(el, wx.TreeCtrl):
            el.Bind(wx.EVT_TREE_SEL_CHANGED, lambda e: v(el.GetItemData(e.GetItem())))
        else:
            el.Bind(k, v)    

def set_nesting_properties(data, el, el_contexts):
    if el_contexts["sizers"]:
        kw = data["sopt"] if "sopt" in data else {}
        szr = el_contexts["sizers"][-1]
        
        for c in szr.GetChildren():
            if c.GetWindow() == el: 
                return
        
        el_contexts["sizers"][-1].Add(el, **kw)    