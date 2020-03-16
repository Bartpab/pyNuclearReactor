def compute_children_diff(old_ch, new_ch):
    ioch = list(enumerate(old_ch))
    inch = list(enumerate(new_ch))

    to_remove = []
    to_patch = []
    
    n_list = inch
    
    for oi, o in ioch:
        f = None
        for ni, n in n_list:
            if o.same(n):
                f = (ni, n)
                break
                
        if f is None:
            to_remove.append((oi, o))
        else:
            to_patch.append((oi, o, *f))
            n_list.remove(f)
    
    # What's left is new
    to_add = n_list[:]
    return to_patch, to_add, to_remove
    
def update_children(old, new, el_contexts):
    from .vnode import patch
    
    old_ch = old.children
    new_ch = new.children
    
    to_patch, to_add, to_remove = compute_children_diff(old_ch, new_ch)
    
    for _, to_r in to_remove:
        to_r.destroy()
    
    nodes = []
    for ai, a in to_add:
        nodes.append((ai, "add", (a,)))
    
    for oi, o, ni, n in to_patch:
        nodes.append((ni, "patch", (o, n, oi)))
        
    nodes = sorted(nodes, key=lambda e: e[0])
    
    for i, instr, args in nodes:
        if instr == "add":
            c = args[0]
            c.set_parent(old)
            c.create_el(el_contexts)            
        else:
            co, cn, oi = args
            patch(co, cn, el_contexts, oi != i)
