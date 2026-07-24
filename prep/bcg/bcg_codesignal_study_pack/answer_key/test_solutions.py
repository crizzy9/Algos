import unittest

from answer_key.solutions import (
    alternating_parity,
    bubble_board,
    cumulative_visits,
    key_changes,
    lunar_phase,
    maximum_subarray,
)


class AnswerKeyTests(unittest.TestCase):
    def test_key_changes(self):
        self.assertEqual(key_changes("aAbBcC"), 2)
        self.assertEqual(key_changes("CodeSignal"), 9)

    def test_lunar_phase(self):
        self.assertEqual(lunar_phase("new", [90, 92, 93, 90], 0, 9), "new")
        self.assertEqual(lunar_phase("full", [3, 5], 1, 1), "waning_crescent")

    def test_bubble_board(self):
        board = [[1, 2, 1], [2, 1, 2], [1, 2, 1]]
        expected = [[0, 0, 0], [0, 2, 0], [2, 2, 2]]
        self.assertEqual(bubble_board(board, [[1, 1]]), expected)

    def test_alternating_parity(self):
        self.assertEqual(alternating_parity([1, 2, 3, 4]), 10)
        self.assertEqual(alternating_parity([1, 3, 2]), 4)

    def test_cumulative_visits(self):
        self.assertEqual(cumulative_visits([100, 200, 150, 400], 450), 2)
        self.assertEqual(cumulative_visits([5, 5], 11), -1)

    def test_maximum_subarray(self):
        self.assertEqual(maximum_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)
        self.assertEqual(maximum_subarray([-8, -3, -6]), -3)


if __name__ == "__main__":
    unittest.main()
