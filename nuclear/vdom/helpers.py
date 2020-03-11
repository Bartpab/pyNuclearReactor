import functools

def helpers(h, self):
    def _h(tag, data, children, events=None):
        return h(self, tag, data, children, events)    
    
    def _it(iterator, el_fn):
        return [el_fn(el) for el in iterator]
    
    def _if(b, if_fn, else_fn=None):
        if b:
            return if_fn()
        elif else_fn:
            return else_fn()
        
        return []
    
    def _f(fn):
        return functools.partial(fn, self)
    
    return _h, _it, _if, _f