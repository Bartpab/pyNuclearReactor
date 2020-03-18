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
def updata_data_to_native(el, data):
    for key, value in data.items():
        if key == "class":
            setattr(el, "style_class", value)
            continue
        
        if key == "key":
            setattr(el, "key", value)
            continue
            
        if key in ("sopt", "key", "class", "sizer"):
            continue
        
        wMethName = "Set" + key[0].upper() + key[1:]
        wMeth = getattr(el, wMethName)
        wMeth(value)
        
def set_data_to_native(el, data):
    for key, value in data.items():
        if key == "class":
            setattr(el, "style_class", value)
            continue
        
        if key == "key":
            setattr(el, "key", value)
            continue
            
        if key in ("sopt", "key", "class"):
            continue
        
        wMethName = "Set" + key[0].upper() + key[1:]
        wMeth = getattr(el, wMethName)
        wMeth(value)

def set_events_to_native(el, events):
    for k, v in events.items():
        if k == "click" and type(el) is wx.Button:
            el.Bind(wx.EVT_BUTTON, v)
        elif k == "click":
            el.Bind(wx.EVT_LEFT_DOWN, v)
        elif k == "change" and type(el) is wx.TextCtrl:
            el.Bind(wx.EVT_TEXT, lambda e: v(e.GetEventObject().GetValue()))
        elif k == "change" and isinstance(el, wx.ComboBox):
            el.Bind(wx.EVT_COMBOBOX, lambda e: v(e.GetEventObject().GetValue()))
        elif k == "change" and isinstance(el, wx.TreeCtrl):
            el.Bind(wx.EVT_TREE_SEL_CHANGED, lambda e: v(el.GetItemData(e.GetItem())))
        else:
            el.Bind(k, v)    

def update_nesting_properties(id, data, el, el_contexts):
    if el_contexts["sizers"]:
        kw = data["sopt"] if "sopt" in data else {}
        szr = el_contexts["sizers"][-1]
        
        for c in szr.GetChildren():
            if c.GetWindow() == el: 
                return
        
        if isinstance(el, wx.Window):
            el.szr_ctrl = el_contexts["sizers"][-1].Add(el, **kw) 
           
def set_nesting_properties(id, data, el, el_contexts):
    if el_contexts["sizers"]:
        kw = data["sopt"] if "sopt" in data else {}
        szr = el_contexts["sizers"][-1]
        
        for c in szr.GetChildren():
            if c.GetWindow() == el: 
                return
        
        if isinstance(el, wx.Window):
            el.szr_ctrl = el_contexts["sizers"][-1].Add(el, **kw)    

def set_font_size(el, val):
    font = el.GetFont()
    font.SetPointSize(val)
    el.SetFont(font)
    
def set_font_colour(el, val):
    rgb = hex_to_rgb(val)
    color = wx.Colour(*rgb) 
    el.SetForegroundColour(color)
    
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def set_background_color(setter, value):
    color = wx.Colour(*hex_to_rgb(value)) 
    setter(color)

def set_margin(el, value):
    if hasattr(el, "szr_ctrl"):
        el.szr_ctrl.SetBorder(value)
    
def set_style_to_native(el, style):
    el.SetFontSize = lambda val: set_font_size(el, val)
    
    if hasattr(el, "SetBackgroundColour"):
        setter = el.SetBackgroundColour
        el.SetBackgroundColour = lambda val: set_background_color(setter, val)
    
    el.SetFontColour = lambda val: set_font_colour(el, val)
    el.SetMargin = lambda val: set_margin(el, val)
    style.add(el)