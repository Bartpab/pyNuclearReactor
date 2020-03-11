def compute_children_diff(old_ch, new_ch):
    to_remove = []
    to_patch = []
    
    n_list = new_ch[:]
    
    for o in old_ch:
        f = None
        for n in n_list:
            if o.same(n):
                f = n
                break
                
        if f is None:
            to_remove.append(o)
        else:
            to_patch.append((o, f))
            n_list.remove(f)
    
    # What's left is new
    to_add = n_list[:]
    return to_patch, to_add, to_remove
    
def update_children(old, new, el_contexts):
    old_ch = old.children
    new_ch = new.children
    
    to_patch, to_add, to_remove = compute_children_diff(old_ch, new_ch)

    for to_r in to_remove:
        to_r.destroy()
    
    for to_a in to_add:
        to_a.set_parent(old)
        to_a.create_el(el_contexts)
    
    for o, v in to_patch:
        o.patch_from(v, el_contexts)