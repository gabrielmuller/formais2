import unittest
from misc import *

class TestMisc(unittest.TestCase):
    def test_set_to_str(self):
        self.assertEqual(set_to_str({"q0", "q1", "01", "02"}),
            "[01, 02, q0, q1]")
        self.assertEqual(set_to_str({"hey", "ho", "let's", "go"}),
            "[go, hey, ho, let's]")

if __name__ == "__main__":
    unittest.main()
