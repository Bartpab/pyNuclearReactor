import sys 
sys.path.append("..")

from nuclear.reactivity import Dep, BaseWatcher, observe, Observable
from nuclear.reactivity import augment

from unittest.mock import MagicMock
import unittest

def cro(**kw):
    obj = type('Object', (), {})()
    
    for k, v in kw.items():
        setattr(obj, k, v)
    
    return obj

class TestReactivity(unittest.TestCase):
    def test_watch_prop_change(self):
        o = cro(a=1)
        self.assertTrue(observe(o))
        
        # After observe call, o should have __ob__ flag
        self.assertTrue(hasattr(o, '__ob__'))
        
        # Create our watcher.
        w = BaseWatcher()
        w.update = MagicMock()
        
        # Add the watcher to the global Dep target tracker.
        Dep.push_target(w)
        
        o.a # Get call, this should add o.a to the targetted watcher (__target__)
        
        Dep.pop_target()
        
        self.assertEqual(len(w.deps), 1) # The watcher should have o.a as dep
        
        o.a = 3 # Set call, should trigger watcher update method
        
        self.assertEqual(w.update.call_count, 1)
        w.deps = []
    
    def test_watch_array_mutation(self):
        o = cro(a=[1,2])
        
        # After observe call, a should have __ob__ flag
        observe(o)
        
        self.assertTrue(hasattr(o.a, '__ob__'))
       
       # Create our watcher.
        w = BaseWatcher()
        w.update = MagicMock()
        
        # Add the watcher to the global Dep target tracker.
        Dep.push_target(w) 
        o.a 
        Dep.pop_target()
        
        self.assertEqual(len(w.deps), 2) # The watcher should have o, o.a as dep
        o.a.append(2)
        self.assertEqual(w.update.call_count, 1)
        
if __name__ == '__main__':
    unittest.main()