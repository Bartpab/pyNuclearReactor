tokens = [    
    "BG_CLOSE_EL",
    "BG_OPEN_EL",
    "END_EL",
    
    "ASSIGN",
    "QUOTE_1",
    "QUOTE_2",

    "ID",
    "PUNCT",
    
    "EXE_FLAG",
    "EV_FLAG",
    "NAMESPACE_FLAG",
    
    "NUMBER",
    "NORMSTRING",
    
    "COMMA",
    "LPAR",
    "RPAR"
]

reserved = {
    'for' : 'FOR',
    'in' : 'IN',
    'if' : 'IF'
}

tokens += reserved.values()

t_PUNCT = r"[.]"

t_ignore = ' \t\n'

t_COMMA = r"[,]"
t_LPAR = r"[(]"
t_RPAR = r"[)]"

t_BG_CLOSE_EL = r'</'
t_BG_OPEN_EL = r'<'
t_END_EL = r'>'
t_NAMESPACE_FLAG = ":"

states = (('str', 'inclusive'),)

def _trace_dynAttr(t):
    if hasattr(t.lexer, "dynAttr") and hasattr(t.lexer, "opQuote") and t.lexer.opQuote == t.value:
        delattr(t.lexer, "dynAttr")
        delattr(t.lexer, "opQuote")
        return t
    
    elif hasattr(t.lexer, "dynAttr"):
        t.lexer.opQuote = t.value
        return t
    
    else:
        t.lexer.lexpos -= 1 # Go back
        t.lexer.push_state('str')

def t_QUOTE_1(t):
    r'["]'
    return _trace_dynAttr(t)

def t_QUOTE_2(t):
    r'[\']'
    return _trace_dynAttr(t)
    
def t_EXE_FLAG(t):
    r"[@]"
    t.lexer.dynAttr = True
    return t

def t_EV_FLAG(t):
    r"[$]"
    t.lexer.dynAttr = True
    return t    
    
def t_ID(t):
    r'[-_A-Za-z0-9]+'
    if t.value in reserved:
        t.type = reserved[ t.value ]
    
    elif t.value.isnumeric():
        t.type = "NUMBER"

    return t

def t_ASSIGN(t):
    r'='
    return t
   
def t_str_NORMSTRING(t):
     r'\"(.*?)\"'
     t.lexer.pop_state()   
     t.value = t.value[1:-1]
     return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t
    
def t_error(t):
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)
    
import ply.lex as lex
lexer = lex.lex()