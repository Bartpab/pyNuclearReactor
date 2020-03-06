import os
from lxml import etree
from ..compiler import compile
import ast

INIT_FILE = """# Automatically generated __init__ 
from .methods       import methods
from .computed      import computed
from .data          import data
from .template      import render
from .rods          import rods

def rod():
    return {
        "template": render,
        "data":     data(),
        "methods":  methods,
        "computed": computed,
        "rods": rods
    }
"""
import re

def get(content, tag_name):
    val = ""
    regex = r"<{tag}>(.*)<\/{tag}>".format(tag=tag_name)    
    
    matches = re.finditer(regex, content, re.MULTILINE | re.DOTALL)
    for matchNum, match in enumerate(matches, start=1):
        val = match.groups()[0]
        
    return val
    
def assemble(rod_file):
    base = os.path.basename(rod_file)
    dir = ".".join(rod_file.split(".")[0:-1])
    
    content = ""
    with open(rod_file, "r") as f:
        content = f.read()
    
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    with open(os.path.join(dir, "__init__.py"), "w") as f:
        f.write(INIT_FILE)
    
    methods_pycode = get(content, "methods")    
    method_names = []
    for c in ast.iter_child_nodes(ast.parse(methods_pycode)):
        if isinstance(c, ast.FunctionDef):
            method_names.append(c.name)
    
    methods_pycode += "\nmethods = {" + ", ".join(['"{key}": {key}'.format(key=m) for m in method_names]) + "}"
    
    with open(os.path.join(dir, "methods.py"), "w") as f:
        f.write(methods_pycode)        
    
    data_pycode = get(content, "data")
    
    with open(os.path.join(dir, "data.py"), "w") as f:
        f.write(data_pycode)        
    

    computed_pycode = get(content, "computed") 
    
    method_names = []
    
    for c in ast.iter_child_nodes(ast.parse(computed_pycode)):
        if isinstance(c, ast.FunctionDef):
            method_names.append(c.name)
    
    computed_pycode += "\ncomputed = {" + ", ".join(['"{key}": {key}'.format(key=m) for m in method_names]) + "}"
    
    with open(os.path.join(dir, "computed.py"), "w") as f:
        f.write(computed_pycode)             
    
    tpl = get(content, "template") 
    tpl_pycode = compile(tpl)
    
    with open(os.path.join(dir, "template.py"), "w") as f:
        f.write(tpl_pycode)  
