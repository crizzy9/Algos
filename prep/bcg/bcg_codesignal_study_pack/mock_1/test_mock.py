import unittest

from mock_1.q1_key_changes import solution as key_changes
from mock_1.q2_lunar_phase import solution as lunar_phase
from mock_1.q3_bubble_board import solution as bubble_board
from mock_1.q4_alternating_parity import solution as alternating_parity


class MockOneTests(unittest.TestCase):
    def test_q1_examples_and_edges(self):
        self.assertEqual(key_changes("aAbBcC"), 2)
        self.assertEqual(key_changes("AaAa"), 0)
        self.assertEqual(key_changes("CodeSignal"), 9)
        self.assertEqual(key_changes("z"), 0)

    def test_q2_examples_and_cycle(self):
        self.assertEqual(lunar_phase("new", [90, 92, 93, 90], 0, 1), "new")
        self.assertEqual(lunar_phase("new", [90, 92, 93, 90], 0, 9), "new")
        self.assertEqual(lunar_phase("full", [3, 5], 1, 1), "waning_crescent")
        self.assertEqual(lunar_phase("last_quarter", [8, 8], 1, 1), "last_quarter")

    def test_q3_center_click(self):
        board = [[1, 2, 1], [2, 1, 2], [1, 2, 1]]
        expected = [[0, 0, 0], [0, 2, 0], [2, 2, 2]]
        self.assertEqual(bubble_board(board, [[1, 1]]), expected)

    def test_q3_empty_click_and_multiple_operations(self):
        board = [[1, 2], [3, 0], [4, 2]]
        self.assertEqual(bubble_board(board, [[1, 1], [2, 1]]), [[1, 0], [3, 0], [4, 2]])

    def test_q4_examples_and_long_run(self):
        self.assertEqual(alternating_parity([1, 2, 3, 4]), 10)
        self.assertEqual(alternating_parity([1, 3, 2]), 4)
        self.assertEqual(alternating_parity([2, 2, 2]), 3)
        self.assertEqual(alternating_parity([7]), 1)


if __name__ == "__main__":
    unittest.main()
