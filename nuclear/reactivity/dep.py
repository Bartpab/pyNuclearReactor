LAST_UID = 0
        
class Dep:
    __target_stack__ = []
    
    @staticmethod
    def push_target(watcher):
        Dep.__target_stack__.append(watcher)
    
    @staticmethod
    def pop_target():
        Dep.__target_stack__.pop(-1)
    
    @staticmethod
    def current_target():
        if Dep.__target_stack__:
            return Dep.__target_stack__[-1]
        return None

    def __init__(self, **kw):
        global LAST_UID
        LAST_UID += 1
        self.id = LAST_UID
        self.subs = []
        self.kw = kw
    
    def sub(self, sub):
        self.subs.append(sub)
    
    def unsub(self, sub):
        self.subs.remove(sub)
    
    def depend(self):
        if Dep.current_target():
            Dep.current_target().add_dep(self)
    
    def notify(self):
        for sub in self.subs:
            sub.update(**self.kw)
