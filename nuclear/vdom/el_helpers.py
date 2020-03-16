def entering_el(el, el_contexts):
    if hasattr(el, "GetSize") and el.GetSizer():
        el_contexts["sizers"].append(el.GetSizer())
    
    el_contexts["stack"].append(el)
    
def leaving_el(el, el_contexts):
    if hasattr(el, "Layout"):
        el.Layout()
        
    if hasattr(el, "GetSize") and el.GetSizer():
        el_contexts["sizers"].pop(-1)
    
    el_contexts["stack"].pop(-1)