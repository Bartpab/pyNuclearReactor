from .dep import Dep
from .watcher import Watcher, BaseWatcher
from .observe import observe
from .mutagen import mutate
from .react   import defineComputed, defineReactive

def inspect_nuclear_props(o):
    return o.__nuclear_props