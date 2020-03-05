from .parser import parse

def push_scope(id, ctx, symbol_table):
    if id not in symbol_table:
        symbol_table[id] = []
    
    symbol_table[id].append(ctx)

def pop_scope(id, symbol_table):
    if id not in symbol_table:
        symbol_table[id] = []
    
    if symbol_table[id]:
        symbol_table[id].pop(-1)
    
def is_local(id, symbol_table):
    if id not in symbol_table:
        symbol_table[id] = []
    
    return len(symbol_table[id]) > 0


ROOT_TPL = """
def render(h, self): {ev_methods}
    return {el}
"""

EL_TPL = """_h("{tag}", {{{data}}}, [{children}], {{{events}}})
"""

FOR_TPL = "*_it({iterable}, lambda {argname}: [{children}])"

EV_TPL = """
    def ev_{id}(e):
        {expr}
"""

def c(ast_node, symbol_table, event_methods):
    print(ast_node)
    node_type, args = ast_node
    
    def _c(node):
        return c(node, symbol_table, event_methods)
    
    if node_type == "root":
        cnode = args
        el=c(cnode, symbol_table, event_methods)
        return ROOT_TPL.format(
           ev_methods="\n".join(event_methods),
           el=el
        )
    
    elif node_type == "el":
        data = args["data"]
        events = args["events"]
        children = args["children"]
        
        return EL_TPL.format(
            tag=args["tag"],
            children=", ".join([_c(cnode) for cnode in children]),
            data=", ".join([_c(dnode) for dnode in data]),
            events=", ".join([_c(enode) for enode in events])
        )
    
    elif node_type == "for":
        argname = args["argname"]
        it_id = args["it_id"]
        children = args["children"]
        
        # ...
        it_node = _c(it_id)
        
        push_scope(argname, [], symbol_table)
        
        r = FOR_TPL.format(
            iterable=it_node,
            argname=argname,
            children=", ".join([_c(cnode) for cnode in children]),
        )
        
        pop_scope(argname, symbol_table)
        
        return r
    
    elif node_type == "event":
        expr = args["value"]
        name = args["name"]
        i = len(event_methods)
        
        push_scope('e', [], symbol_table)
        event_methods.append(EV_TPL.format(id=i, expr=_c(expr)))
        pop_scope('e', symbol_table)
        
        fn_id = "ev_{id}".format(id=i)
        
        return "\"{key}\" : {value}".format(
            key=name,
            value=fn_id
        )
        
    elif node_type == "data":
        name = args["name"]
        value = args["value"]
        
        return "\"{key}\" : {value}".format(
            key=name,
            value=_c(value)
        )
    
    elif node_type == "statement":
        return _c(args)
    
    elif node_type == "assign":
        return "{l} = {r}".format(l=_c(args["l"]), r=_c(args["r"]))
    
    elif node_type == "expr":
        return _c(args)
    
    elif node_type == "id":
        id = args["value"]
        
        varname = id.split(".")[0]
        if is_local(varname, symbol_table):
            return id
        else:
            return "self." + id
    
    elif node_type == "primary":
        value = args["value"]
        return value
    
    else:
        return ""
    
def compile(txt):
    symbol_table = {}
    event_methods = []
    ast = parse(txt)
    return c(ast, symbol_table, event_methods)
    