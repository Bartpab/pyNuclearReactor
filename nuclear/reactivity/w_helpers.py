from . import inspect_nuclear_props

def deep(observable):
    """
        Make the observable and all its attribute as dependencies of the current Watcher
    """
    for k, d in inspect_nuclear_props(observable).items(): 
        d.dep.depend()
        deep(getattr(observable, k))
        
    return observable