import os
from lxml import etree
from ..compiler import compile
import ast

INIT_FILE = """# Automatically generated __init__ 
from .methods       import methods
from .watch         import watch
from .computed      import computed
from .data          import data
from .template      import render
from .rods          import rods

def rod():
    return {{
        "id":       "{id}",
        "template": render,
        "data":     data(),
        "methods":  methods,
        "computed": computed,
        "watch":    watch,
        "rods":     rods
    }}
"""
import re
import autopep8

def format(pycode):
    return autopep8.fix_code(pycode, options={'aggressive': 2})

def get(content, tag_name):
    val = ""
    regex = r"<{tag}>(.*)<\/{tag}>".format(tag=tag_name)    
    
    matches = re.finditer(regex, content, re.MULTILINE | re.DOTALL)
    for matchNum, match in enumerate(matches, start=1):
        val = match.groups()[0]
        
    return val

def parse_watch(content):
    regex = r"\{(.*?)\}[ ]*=>[ ]*\{(.*?)\}"

    matches = re.finditer(regex, content, re.MULTILINE | re.DOTALL)
    
    watchers = []
    
    for matchNum, match in enumerate(matches, start=1):
        watch_expr = match.groups()[0].strip()
        logic_expr = match.groups()[1].strip()
        
        watch_fn = "lambda self: {}".format(watch_expr)
        logic_fn = "lambda self, value, old_value: {}".format(logic_expr)
        

        watchers.append("({}, {})".format(watch_fn, logic_fn))
        
    return """
from nuclear.reactivity.w_helpers import *
watch=[{}]
""".format(", ".join(watchers))
    
def assemble(rod_file):
    base = os.path.basename(rod_file)
    dir = ".".join(rod_file.split(".")[0:-1])
    
    id = dir.replace("/", "::").replace("\\", "::")
    
    content = ""
    with open(rod_file, "r") as f:
        content = f.read()
    
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    with open(os.path.join(dir, "__init__.py"), "w") as f:
        f.write(format(INIT_FILE.format(id=id)))
    
    methods_pycode = get(content, "methods")    
    method_names = []
    for c in ast.iter_child_nodes(ast.parse(methods_pycode)):
        if isinstance(c, ast.FunctionDef):
            method_names.append(c.name)
    
    methods_pycode += "\nmethods = {" + ", ".join(['"{key}": {key}'.format(key=m) for m in method_names]) + "}"
    
    with open(os.path.join(dir, "methods.py"), "w") as f:
        f.write(format(methods_pycode))

    watch_pycode = parse_watch(
        get(content, "watch")
    ) 
    
    with open(os.path.join(dir, "watch.py"), "w") as f:
        f.write(format(watch_pycode)) 
      
    data_pycode = get(content, "data")
    with open(os.path.join(dir, "data.py"), "w") as f:
        f.write(format(data_pycode))    
    

    computed_pycode = get(content, "computed") 
    
    method_names = []
    
    for c in ast.iter_child_nodes(ast.parse(computed_pycode)):
        if isinstance(c, ast.FunctionDef):
            method_names.append(c.name)
    
    computed_pycode += "\ncomputed = {" + ", ".join(['"{key}": {key}'.format(key=m) for m in method_names]) + "}"
    with open(os.path.join(dir, "computed.py"), "w") as f:
        f.write(computed_pycode)             
 
    rods_pycode = get(content, "rods")
    rods_names = []
    for c in ast.iter_child_nodes(ast.parse(rods_pycode)):
        if isinstance(c, ast.Assign):
            rods_names.append(c.targets[0].id)
    rods_pycode += "\nrods = {" + ", ".join(['"{key}": {key}'.format(key=m) for m in rods_names]) + "}"
    
    with open(os.path.join(dir, "rods.py"), "w") as f:
        f.write(format(rods_pycode))             
    
    tpl = get(content, "template") 
    tpl_pycode = "import functools\n{}".format(compile(tpl))
    
    with open(os.path.join(dir, "template.py"), "w") as f:
        f.write(format(tpl_pycode))
