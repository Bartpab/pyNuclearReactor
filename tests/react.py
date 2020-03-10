import sys 
sys.path.append("..")

from nuclear.reactivity import Dep, BaseWatcher, Watcher, observe
from nuclear.reactivity import inspect_nuclear_props
from nuclear.reactivity import defineComputed

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
        q = cro(g=2)
        
        observe(q)
        self.assertTrue(observe(o))
        
        o.a = 10
        # After observe call, o should have __ob__ flag
        self.assertTrue(hasattr(o, '__ob__'))
        self.assertTrue(hasattr(o, '__nuclear_props'))
        self.assertTrue("a" in getattr(o, "__nuclear_props"))
        
        # Create our watcher.
        w = BaseWatcher()
        w.update = MagicMock()
        
        # Add the watcher to the global Dep target tracker.
        Dep.push_target(w)
        o.a # Get call, this should add o.a to the targetted watcher (__target__)
        Dep.pop_target()
        
        self.assertEqual(len(inspect_nuclear_props(o)["a"].dep.subs), 1)
        sub = inspect_nuclear_props(o)["a"].dep.subs[0]
        self.assertEqual(w, sub)
        self.assertEqual(len(w.deps), 1) # The watcher should have o.a as dep
        self.assertEqual(w.update.call_count, 0)
        o.a = 3 # Set call, should trigger watcher update method
        
        self.assertEqual(w.update.call_count, 1)
        w.deps = []
    
    def test_watch_array_mutation(self):
        
        o = cro(a=[1,2])
        
        # After observe call, a should have __ob__ flag
        observe(o)
        
        self.assertTrue("a" in inspect_nuclear_props(o))
        self.assertEqual(o.a.__class__.__name__, "ObservableList")
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
    
    def test_observe_list(self):
        return
        o = cro(a=[cro(c=1), cro(d=2)])
        observe(o)
        pass
        
    def test_watch_computed(self):
        
        o = cro(a=1)
        self.assertTrue(observe(o))
        
        # Define a computed value
        defineComputed(o, "b", lambda o: o.a + 1)
        
        # Check that b is a computed value
        self.assertTrue(inspect_nuclear_props(o)["b"].__class__.__name__, "ComputedProperty")

        o.b
        o.a = 2
        
        a_dep       = inspect_nuclear_props(o)["a"].dep
        b_watcher   = inspect_nuclear_props(o)["b"].watcher
        
        self.assertEqual(b_watcher.deps[0], a_dep)
    
        Watcher.run_all()
        
        self.assertEqual(o.b, 3)
        
if __name__ == '__main__':
    unittest.main()