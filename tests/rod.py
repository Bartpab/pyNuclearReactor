from nuclear.vnode import helpers

def render(h, self): 
    _h, _it, _if, _f  = helpers(h, self) 
    return _h("panel", {"sizer_options" : {"flag" : "test", "proportion" : 1}}, [*_it(self.iterator, lambda el: [*_if(el, lambda: [])])], {})

