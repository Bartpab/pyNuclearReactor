from .helpers import is_class, is_tag
    
class StyleRule:
    def __init__(self, selector_fn, rule_fn):
        self.selector_fn = selector_fn
        self.rule_fn = rule_fn
        
    def is_applicable(self, el):
        return self.selector_fn(el)
    
    def apply(self, el):
        self.rule_fn(el)
        
class StyleEngine:   
    __new__   = []
    __els__   = []
    
    __rules__ = []
    
    @staticmethod
    def add(el):
        if el not in StyleEngine.__new__:
            StyleEngine.__new__.append(el)
            StyleEngine.run_all()
    
    @staticmethod
    def remove(el):
        if el in StyleEngine.__new__:
            StyleEngine.__new__.remove(el)        
        
        if el in StyleEngine.__els__:
            StyleEngine.__els__.remove(el)
            
    @staticmethod
    def run_all():
        while StyleEngine.__new__:
            el = StyleEngine.__new__.pop(-1)
            StyleEngine.apply(el)
            StyleEngine.__els__.append(el)
    
    @staticmethod
    def define_rule(rule):
        StyleEngine.__rules__.append(rule)
    
    @staticmethod
    def apply(el):
        for is_applicable, apply in StyleEngine.__rules__:
            if is_applicable(el):
                apply(el)
        