
from nuclear.style.helpers import is_class, is_tag

_it = is_tag
_ic = is_class

rulesets = ((lambda el: any([all([_it("Test", el),_ic("ClassBar", el)])]), lambda el: [el.SetFoo(0)]))
