from .dep import Dep
from .watcher import Watcher, BaseWatcher
from .observe import observe
from .patch   import reactify
from .react   import defineComputed, defineReactive

def inspect_nuclear_props(o):
    return o.__nuclear_props