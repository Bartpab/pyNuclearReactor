from .dep import Dep
from ..log import log

class BaseWatcher:
    def __init__(self):
        self.deps = []
        self.deps_ids = []
    
    def add_dep(self, dep):
        self.deps.append(dep)
        dep.sub(self)
    
    def update(self):
        pass
        
class Watcher(BaseWatcher):
    __queue__ = []
    
    @staticmethod
    def add(w):
        if w not in Watcher.__queue__:
            Watcher.__queue__.append(w)
    
    @staticmethod
    def remove(w):
        if w in Watcher.__queue__:
            Watcher.__queue__.append(w)
    
    @staticmethod
    def run_all():
        while Watcher.__queue__:
            w = Watcher.__queue__.pop(-1)
            w.run()
        
    def __init__(self, data, fn, cb=None, options=None):
        BaseWatcher.__init__(self)

        self.new_deps = []
        self.new_deps_ids = []
        self.deps_ids = []
        
        self.data = data
        self.getter = fn
        self.cb = cb
        
        self.value = None
        self.options = options if options else {}
       
    def add_dep(self, dep):
        dep_id = dep.id
        
        if not dep_id in self.new_deps_ids:
            self.new_deps_ids.append(dep_id)
            self.new_deps.append(dep)
            
            if not dep_id in self.deps_ids:
                self.deps_ids.append(dep_id)
                self.deps.append(dep)
                dep.sub(self)

    def cleanup_deps(self):
        for dep in self.deps:
            if not dep.id in self.new_deps_ids:
                dep.unsub(self)
        
        self.deps_ids = self.new_deps_ids[:]
        self.new_deps_ids = []
        self.deps = self.new_deps[:]
        self.new_deps = []
    
    def run(self):
        value = self.get()
        
        old_value = self.value
        self.value = value
        
        if self.cb:
            self.cb(value, old_value)        
    
    def update(self, **kw):
        log.watcher_update(self, kw)        
        Watcher.add(self)
    
    def destroy(self):
        self.new_deps_ids = []
        self.new_deps_ids = []
        self.cleanup_deps()
        Watcher.remove(self)
    
    def get(self):
        Dep.push_target(self)
        value = self.getter(self.data)
        Dep.pop_target()
        self.cleanup_deps()
        return value