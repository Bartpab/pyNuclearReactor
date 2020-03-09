def render(h, self):
    return h(
        self, 
        self.g_router.get_current_route(), 
        self.g_router.get_current_route_args(), 
        [], 
        {}
    )

def get_rod(self, key):
    return self.g_router.routes[key]
    
class Router:
    def __init__(self):
        self.routes = {}
        self.url = "default"
    
    def go_to(self, url):
        self.url = url
    
    def define(self, route, rod):
        self.routes[route] = rod
    
    def get_current_route(self):
        return self.url
    
    def get_current_rod(self):
        return self.routes[self.url]
    
    def get_current_route_args(self):
        return {}
        
    def as_rod(self):
        return {
            "template": render,
            "data": {
                "g_router": self
            },
            "methods":  {
                "get_rod": get_rod
            },
            "computed": {},
            "rods": {}            
        }

