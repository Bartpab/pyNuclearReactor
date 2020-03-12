tokens = [    
    "ID",
    
    "NUMBER",
    "NORMSTRING",
    
    "BG_BLOCK",
    "END_BLOCK",
    
    'PUNCT',
    'SEP',
    'ASSIGN'
]

reserved = {

}

tokens += reserved.values()
t_ignore = ' \t\n'
t_ignore_COMMENT = r'/\*(.*?)\*/'

t_BG_BLOCK = r"[{]"
t_END_BLOCK = r"[}]"
t_PUNCT = r"[.]"
t_SEP   = r'[;]'
t_ASSIGN = r'[:]'

def t_ID(t):
    r'[-_A-Za-z0-9]+'
    if t.value in reserved:
        t.type = reserved[ t.value ]
    
    elif t.value.isnumeric():
        t.type = "NUMBER"

    return t

def t_NORMSTRING(t):
     r'\"(.*?)\"'
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