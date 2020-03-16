import os

from .parser import parse
from .helpers import is_class, is_tag

import functools

STYLE_FN ="""
from nuclear.style.helpers import is_class, is_tag, is_state

_it = is_tag
_ic = is_class
_st = is_state

{rulesets}
"""
def c(ast_node):
    node_type, args = ast_node
    
    def _c(node):
        return c(node)
    
    if node_type == "rulesets":
        rulesets = "rulesets = [{}]".format(
            ", ".join([_c(r) for r in args])
        )
        return STYLE_FN.format(rulesets=rulesets)
    
    if node_type == "ruleset":
        return "({sel}, {block})".format(
            sel=_c(args['selector']),
            block=_c(args['block'])
        )
        
    # Selector function compiler
    elif node_type == "selector":
        el_selectors = [_c(el_selector) for el_selector in args]
        
        return "lambda el: any([{}])".format(",".join(
                [_c(sub_selector) for sub_selector in args]
            )
        )
    
    elif node_type == "el-selector":
        return "all([{}])".format(",".join(
                [_c(sub_selector) for sub_selector in args]
            )
        )    
    
    elif node_type == 'class-selector':
        return "_ic(\"{args}\", el)".format(args=args)

    elif node_type == 'tag-selector':
        return "_it(\"{args}\", el)".format(args=args)
    
    elif node_type == 'state-selector':
        return "_st(\"{args}\", el)".format(args=args)
    
    # Rule logic function building
    elif node_type == 'block':
        return "lambda el: {}".format(_c(args))
    
    elif node_type == 'decls':
        return "[{}]".format(
            ",".join([_c(decl) for decl in args])
        )

    elif node_type == 'decl':
        property = args['property']
        value = args['value']
        wMethName = "Set" + property[0].upper() + property[1:]
        return "el.{setter}({val})".format(
            setter=wMethName,
            val=value
        )
    else:
        return None
    
def compile(txt):
    ast = parse(txt)
    return c(ast)
