from .lexer import lexer, tokens

def p_empty(p):
    'empty :'
    pass
    
def p_attrs(p):
    '''attrs : attrs attr 
             | attr 
             | empty '''
     
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]

def p_fn(p):
    '''
        fn : id LPAR expr RPAR
    '''
    p[0] = ("fn", {"name": p[1], "args": [p[3]]})

def p_binop_expr(p):
    '''
        binop_expr : expr PIPE expr
    '''
    p[0] = ("binop_expr", {"l": p[1], "op": p[2], "r": p[3]})    
    
def p_expr(p):
    '''
        expr : id 
             | fn
             | binop_expr
    '''
    p[0] = ("expr", p[1])
    
def p_assign_statement(p):
    '''
        assign_statement : id ASSIGN expr
    '''
    p[0] = (
        "assign",
        {
            "l": p[1],
            "r": p[3]
        }
    )
    
def p_statement(p):
    '''
        statement : assign_statement 
                  | expr
    '''
    p[0] = ("statement", p[1])
    
def p_static_attr(p):
    '''static_attr : tag_name ASSIGN QUOTE_1 NUMBER QUOTE_1
           | tag_name ASSIGN QUOTE_2 NUMBER QUOTE_2
           | tag_name ASSIGN NORMSTRING
    '''     
    
    v = p[4] if len(p) == 6 else p[3]
    
    v = ("primary", {"value": v})
    
    p[0] = (
        "data", 
        {   
            "name": p[1],
            "is_exec": False,
            "value": v
        }
    )

def p_tag_name(p):
    '''
        tag_name : ID
                | tag_name NAMESPACE_FLAG ID
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + ":" + p[3]

   
def p_exec_attr(p):
    '''exec_attr : EXE_FLAG tag_name ASSIGN QUOTE_1 expr QUOTE_1
           | EXE_FLAG tag_name ASSIGN QUOTE_2 expr QUOTE_2
    '''    
    p[0] = (
        "data", 
        {
            "name": p[2],
            "is_exec": True,
            "value": p[5]
        } 
    )
    
def p_event_attr(p):
    '''event_attr : EV_FLAG ID ASSIGN QUOTE_1 statement QUOTE_1
           | EV_FLAG ID ASSIGN QUOTE_2 statement QUOTE_2
    '''    
    p[0] = (
        "event", 
        {
            "name": p[2],
            "value": p[5]
        } 
    )

def p_attr(p):
    '''attr : static_attr
           | exec_attr
           | event_attr
    '''
    p[0] = p[1]

def p_id(p):
    '''
        id : id PUNCT ID
            | ID
    ''' 
    if len(p) == 2:
        p[0] = ("id", {"value": p[1]})
    else:
        p[0] = (
            "id", {"value": p[1][1]["value"] + "." + p[3]}
        )
    
def p_end_el(p):
    '''
        end_el : BG_CLOSE_EL ID END_EL
    '''
    p[0] = None
    
def p_op_el(p):
    '''op_el : BG_OPEN_EL ID attrs END_EL
    '''

    data = []
    events = []

    for type, args in p[3]:
        if type == "event":
            events.append((type, args))
        else:
            data.append((type, args))
    
    p[0] = (
        "op-el", {
            "tag": p[2],
            "data": data,
            "events": events
        }
    )

def p_for_el(p):
    '''
        for_el : BG_OPEN_EL FOR ID IN id END_EL els BG_CLOSE_EL FOR END_EL
    '''
    p[0] = ("for", {
        "it_id": p[5],
        "argname": p[3],
        "children": p[7]
    })
    
def p_if_el(p):
    '''
        if_el : BG_OPEN_EL IF expr END_EL els BG_CLOSE_EL IF END_EL
    '''
    p[0] = ("if", {
        "condition": p[3],
        "children": p[5]
    })
        
def p_normal_el(p):
    '''
       normal_el : op_el els end_el 
    '''

    p[0] = ("el", {
        **p[1][1],
        "children": p[2]
    })

def p_els(p):
    '''
        els : els el
            | el
            | empty
    '''
    if len(p) == 2:
        p[0] = [p[1]] if p[1] else []
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]
    
def p_el(p):
    '''el : normal_el
          | for_el 
          | if_el
    '''
    p[0] = p[1]

def p_error(p):
    print(f"Syntax error at {p.value!r}, (L:{p.lineno!r}, I:{p.lexpos!r})")
   
import ply.yacc as yacc
parser = yacc.yacc(start='normal_el') 

def parse(txt):
    lexer.input(txt)
    node = parser.parse(txt, lexer=lexer)
    return ("root", node)