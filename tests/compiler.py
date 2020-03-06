import sys 
sys.path.append("..")
from pathlib import Path

from nuclear.compiler import compile

import unittest

class TestPack(unittest.TestCase):
    def test_compile(self):
        txt = Path("rod.trod").open("r").read()
        pyCode = compile(txt)
        exec(pyCode)

if __name__ == '__main__':
    unittest.main()