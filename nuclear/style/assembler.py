import os
from . import compile

def assemble(style_file):
    base = os.path.basename(".".join(style_file.split(".")[0:-1]))
    dir = os.path.dirname(style_file)
    
    content = ""
    with open(style_file, "r") as f:
        content = f.read()
        
    with open(os.path.join(dir, "{}.py".format(base)), "w") as f:
        f.write(compile(content))