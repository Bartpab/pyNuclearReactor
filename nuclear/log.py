class Log:
    def __init__(self):
        pass
    
    def log(self, msg):
        print("[NuclearReactor] " + msg)
    
    def create_assembly(self, assembly, props, events):
        self.log("[CREATE] {}, props={}".format(
            str(assembly),
            str(props)
        ))
    
    def assembly_render(self, assembly):
        self.log("[RENDER] {}".format(
            str(assembly)
        ))        
    
    def assembly_patch(self, assembly, new_assembly):
        self.log("[PATCH] {}, props={}".format(
            str(assembly),
            new_assembly.props
        ))
    
    def assembly_event_emitted(self, assembly, event_name, args):
        self.log("[EVENT] \"{}\" from {}, args={}".format(
            event_name,
            str(assembly),
            str(args)
        ))
    
    def assembly_data_props_changed(self, assembly, key, value):
        self.log("[DATA] {} {} => {}".format(str(assembly), key, value))
    
    def watcher_update(self, watcher, kw, already_scheduled=False):
        if "name" in watcher.options and "src" in kw and "key" in kw:
            self.log("[{}] {} reason={}.{}".format(
                "UPDATE" if not already_scheduled else "UPDATE BIS",
                watcher.options["name"], 
                str(kw["src"]), 
                kw["key"])
            )
            
log = Log()