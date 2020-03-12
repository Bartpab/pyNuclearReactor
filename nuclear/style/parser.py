from .lexer import lexer, tokens

def p_rulesets(p):
    '''
        rulesets : ruleset
                 | rulesets ruleset
    '''
    if len(p) == 2:
        p[0] = ('rulesets', [p[1]])
    
    else:
        p[0] = ('rulesets', p[1][1] + [p[2]])
        
def p_ruleset(p):
    'ruleset : selector block'
    p[0] = ('ruleset', {'selector': p[1], 'block': p[2]})
    
# Selector part
def p_selector(p):
    '''
        selector : selector el_selector 
                | el_selector
    '''
    if len(p) == 2:
        p[0] = ('selector', [p[1]])
    
    else:
        p[0] = ('selector', p[1][1] + [p[2]])

def p_el_selector(p):
    '''
        el_selector : tag_selector
                    | el_selector class_selector
    '''
    if len(p) == 2:
        p[0] = ('el-selector', [p[1]])
    else:
        p[0] = ('el-selector', p[1][1] + [p[2]])
        
def p_tag_selector(p):
    'tag_selector : ID'
    p[0] = ('tag-selector', p[1])

def p_class_selector(p):
    'class_selector : PUNCT ID'
    p[0] = ('class-selector', p[2])

# Logic of the rule
def p_decls(p):
    '''
        decls : decls SEP decl 
              | decl
    '''
    if len(p) == 2:
        p[0] = ('decls', [p[1]])
    else:
        p[0] = ('decls', p[1] + [p[3]])

def p_decl(p):
    '''
        decl : property ASSIGN value
    '''
    p[0] = ('decl', {'property': p[1], 'value': p[3]})

def p_value(p):
    '''
        value : NORMSTRING
              | NUMBER
    '''
    p[0] = p[1]
    
def p_property(p):
    '''
        property : ID
    '''
    p[0] = p[1]
    
def p_block(p):
    'block : BG_BLOCK decls END_BLOCK'
    p[0] = ('block', p[2])
    
def p_error(p):
    print(f"Syntax error at {p.value!r}, (L:{p.lineno!r}, I:{p.lexpos!r})")
   
import ply.yacc as yacc
parser = yacc.yacc(start='rulesets') 

def parse(txt):
    lexer.input(txt)
    node = parser.parse(txt, lexer=lexer)
    return node