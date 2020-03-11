def render(h, self):
    return h(
        self, 
        self.router.get_current_route(), 
        self.router.get_current_route_args(), 
        [], 
        {}
    )

def get_rod(self, key):
    return self.router._routes[key]
        
class Router:
    def __init__(self):
        self._routes = {}
        self.url = "default"
        self.args = {}
    
    def go_to(self, url, **kw):
        self.url = url
        self.args = kw
    
    def define(self, route, rod):
        self._routes[route] = rod
    
    def get_current_route(self):
        return self.url
    
    def get_current_rod(self):
        return self._routes[self.url]
    
    def get_current_route_args(self):
        return self.args
    
    def __copy__(self):
        return RouterPtr(self)
        
    def as_rod(self):
        return {
            "template": render,
            "data": {
                "router": self
            },
            "methods":  {
                "get_rod": get_rod
            },
            "computed": {},
            "rods": {}            
        }

