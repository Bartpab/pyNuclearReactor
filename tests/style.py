import sys 
sys.path.append("..")
sys.path.append(".")

from nuclear.style import compile
from unittest.mock import MagicMock
import unittest

def cro(name, **kw):
    obj = type(name, (), {})()
    
    for k, v in kw.items():
        setattr(obj, k, v)
    
    return obj

test_css = """
Test.ClassBar 
{
    foo: 0
}
"""
class TestReactivity(unittest.TestCase):
    def test_watch_prop_change(self):
        # Create our watcher.
        el = cro("Test", style_class="ClassBar")
        el.SetFoo = MagicMock()
        
        py_rulesets = compile(test_css)
        
        with open("style_rules.py", "w") as f:
            f.write(py_rulesets)
        
        from style_rules import rulesets
        
        self.assertEqual(len(rulesets), 1)
        
        selector, rule = rulesets[0]
        self.assertTrue(selector(el))
        
        rule(el)     
        el.SetFoo.assert_called_once_with(0)
    
        
if __name__ == '__main__':
    unittest.main()