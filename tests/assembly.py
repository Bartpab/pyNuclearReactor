import sys 
sys.path.append("..")
from pathlib import Path

from nuclear.assembly import assemble

import unittest

class TestAssembly(unittest.TestCase):
    def test_pack(self):
        assemble("app.rod")

if __name__ == '__main__':
    unittest.main()