def is_tag(tag, el):
    return tag == type(el).__name__

def is_class(style_cls, el):
    cls = None if not hasattr(el, "style_class") else el.style_class
    
    if cls is None:
        return False
    
    return style_cls == cls

def is_state(state, el):
    return hasattr(el, state) and getattr(el, state)