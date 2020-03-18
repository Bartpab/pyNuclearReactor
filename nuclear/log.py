class Log:
    def __init__(self):
        pass
    
    def log(self, msg):
        print("[NuclearReactor] " + msg)
    
    def create_assembly(self, assembly, props, events):
        self.log("[CREATE] Creating {}, props={}".format(
            assembly.name,
            str(props)
        ))
    
    def assembly_patch(self, assembly, new_assembly):
        self.log("[PATCH] Patching {}|{}, props={}".format(
            assembly.name,
            new_assembly.name,
            new_assembly.props
        ))
    
    def assembly_event_emitted(self, assembly, event_name, args):
        self.log("[EVENT] Event {} emitted from {}, args={}".format(
            event_name,
            str(assembly),
            str(args)
        ))
    
    def watcher_update(self, watcher, kw):
        if "name" in watcher.options and "src" in kw and "key" in kw:
            self.log("[UPDATE] Update {} because of {}.{}".format(watcher.options["name"], str(kw["src"]), kw["key"]))
            
log = Log()