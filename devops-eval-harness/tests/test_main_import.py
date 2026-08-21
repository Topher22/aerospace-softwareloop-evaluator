import importlib
import os
import sys
import unittest


class MainImportTest(unittest.TestCase):
    def test_main_module_imports(self):
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        module = importlib.import_module("main")
        self.assertTrue(callable(module.main))


if __name__ == "__main__":
    unittest.main()
