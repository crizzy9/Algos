import unittest

from extras.cumulative_visits import solution as cumulative_visits
from extras.maximum_subarray import solution as maximum_subarray


class ExtraProblemTests(unittest.TestCase):
    def test_cumulative_visits(self):
        self.assertEqual(cumulative_visits([100, 200, 150, 400], 450), 2)
        self.assertEqual(cumulative_visits([5, 5], 11), -1)
        self.assertEqual(cumulative_visits([10], 1), 0)

    def test_maximum_subarray(self):
        self.assertEqual(maximum_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)
        self.assertEqual(maximum_subarray([-8, -3, -6]), -3)
        self.assertEqual(maximum_subarray([7]), 7)


if __name__ == "__main__":
    unittest.main()
