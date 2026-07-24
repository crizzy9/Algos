"""T9 input method.

T9 is a type of keypad commonly seen on mobile phones (see the keypad below).
To type with T9, a user enters digits and a program (also called an input
method) translates the input into English words with the help of a dictionary
stored on the device.

    2: abc    3: def    4: ghi
    5: jkl    6: mno    7: pqrs
    8: tuv    9: wxyz

Our task is to implement this input method.

Inputs
------
The main function will be given two inputs:

* ``input_digits``: an integer array containing only digits 2-9. Its length is
  up to 25.
* ``valid_words``: a string array defining a list of valid English words. It
  contains up to 50 words.

Outputs
-------
Return a 2D string array of all the possible word combinations that the given
input can be mapped to. More specifically, the return value has the format

    [<word combination 1>, <word combination 2>, ...]

where each ``<word combination>`` is an array of words representing either one
word or a list of words into which the input digits can be translated.

For example, suppose ``"cat"`` is a valid word and the input is ``228``. The
only word combination in this case is ``["cat"]``.

In a different example, suppose all of ``"some"``, ``"time"``, and
``"sometime"`` are valid words and the input is ``76638463``. Both
``["some", "time"]`` and ``["sometime"]`` are valid word combinations.

Examples
--------
Example 1: each word combination contains only a single word.

    input_digits: [2, 2, 8]
    valid_words: ["act", "bat", "cat", "acd", "test"]
    output: [["act"], ["bat"], ["cat"]]

Example 2: a word combination can contain multiple words.

    input_digits: [7, 6, 6, 3, 8, 4, 6, 3]
    valid_words: ["some", "time", "rome", "sometime", "so", "me"]
    output: [
        ["rome", "time"],
        ["so", "me", "time"],
        ["some", "time"],
        ["sometime"],
    ]

Note that the total length of the words in a word combination must match the
size of ``input_digits``. In other words, each input digit must be accounted
for once and only once by a character from a word combination.

Limits and CodeSignal types
---------------------------
* Execution time limit: 4 seconds (Python 3)
* Memory limit: 1 GB
* [input] array.integer input_digits
* [input] array.string valid_words
* [output] array.array.string

The screenshots do not state an output-ordering rule. Their expected outputs
are lexicographically ordered; the local test runner below compares results
without regard to the outer array's order.
"""


def solution(input_digits, valid_words):
    """Return every valid word combination for ``input_digits``."""

    source = {
        2: ["a", "b", "c"],
        3: ["d", "e", "f"],
        4: ["g", "h", "i"],
        5: ["j", "k", "l"],
        6: ["m", "n", "o"],
        7: ["p", "q", "r", "s"],
        8: ["t", "u", "v"],
        9: ["w", "x", "y", "z"],
    }

    combos = {}

    n = len(input_digits)
    possible_words = []
    new_possible_words = []
    split_words = []
    new_split_words = []
    for i in range(n):
        possible_words = valid_words
        letters = source[input_digits[i]]
        print("i:", i)
        for word in possible_words:
            if i < len(word) and word[i] in letters:
                new_possible_words.append(word)
            else:
                new_split_words.append(word)

        possible_words = new_possible_words
        new_possible_words = []
        split_words = new_split_words
        new_split_words = []

        print("possible_words", possible_words)
        print("split_words", split_words)

    out = [[word] for word in possible_words]

    return out


def soln(input_digits, valid_words):
    source = {
        2: ["a", "b", "c"],
        3: ["d", "e", "f"],
        4: ["g", "h", "i"],
        5: ["j", "k", "l"],
        6: ["m", "n", "o"],
        7: ["p", "q", "r", "s"],
        8: ["t", "u", "v"],
        9: ["w", "x", "y", "z"],
    }

    n = len(input_digits)
    possible_words = []
    new_possible_words = []
    split_words = []
    new_split_words = []
    for i in range(n):
        possible_words = valid_words
        letters = source[input_digits[i]]
        print("i:", i)
        for word in possible_words:
            if i < len(word) and word[i] in letters:
                new_possible_words.append(word)
            else:
                if len(word) == i:
                    x = [word]
                    out = soln(input_digits[i:], valid_words)
                    print("out:", out)

                new_split_words.append(word)

        possible_words = new_possible_words
        new_possible_words = []
        split_words = new_split_words
        new_split_words = []

        print("possible_words", possible_words)
        print("split_words", split_words)

    out = [[word] for word in possible_words]

    return out


def optimal_solution(input_digits, valid_words):
    """Return all valid T9 word splits using a trie and memoized recursion.

    The trie makes it cheap to find dictionary words whose T9 encodings match
    the digits at a given position. Memoization ensures that the combinations
    for each suffix of ``input_digits`` are computed only once.
    """
    letter_to_digit = {
        letter: digit
        for digit, letters in {
            2: "abc",
            3: "def",
            4: "ghi",
            5: "jkl",
            6: "mno",
            7: "pqrs",
            8: "tuv",
            9: "wxyz",
        }.items()
        for letter in letters
    }

    digits = tuple(input_digits)
    if not digits:
        return []

    words_key = "words"
    trie = {}

    # Multiple words can have the same T9 encoding, so terminal trie nodes
    # store a list rather than a single word.
    for word in sorted(set(valid_words)):
        if not word or len(word) > len(digits):
            continue

        node = trie
        for letter in word:
            node = node.setdefault(letter_to_digit[letter], {})
        node.setdefault(words_key, []).append(word)

    memo = {}

    def combinations_from(start):
        if start == len(digits):
            return ((),)

        if start in memo:
            return memo[start]

        combinations = []
        node = trie

        # Walk the trie and input together. Every terminal node represents a
        # possible word boundary, so solve the remaining suffix from there.
        for end in range(start, len(digits)):
            node = node.get(digits[end])
            if node is None:
                break

            for word in node.get(words_key, ()):
                for suffix in combinations_from(end + 1):
                    combinations.append((word, *suffix))

        memo[start] = tuple(combinations)
        return memo[start]

    result = [list(combination) for combination in combinations_from(0)]
    result.sort()
    return result


# The first two cases are the examples from the problem statement. The rest
# are additional cases for exercising boundary behavior and word splitting.
TEST_CASES = [
    # {
    #     "name": "provided example: single-word combinations",
    #     "input_digits": [2, 2, 8],
    #     "valid_words": ["act", "bat", "cat", "acd", "test"],
    #     "expected": [["act"], ["bat"], ["cat"]],
    # },
    # {
    #     "name": "provided example: multi-word combinations",
    #     "input_digits": [7, 6, 6, 3, 8, 4, 6, 3],
    #     "valid_words": ["some", "time", "rome", "sometime", "so", "me"],
    #     "expected": [
    #         ["rome", "time"],
    #         ["so", "me", "time"],
    #         ["some", "time"],
    #         ["sometime"],
    #     ],
    # },
    # {
    #     "name": "empty",
    #     "input_digits": [],
    #     "valid_words": [],
    #     "expected": [],
    # },
    # {
    #     "name": "no valid combination",
    #     "input_digits": [2, 3],
    #     "valid_words": ["cat", "dog", "me"],
    #     "expected": [],
    # },
    # {
    #     "name": "single digit ignores nonmatching and longer words",
    #     "input_digits": [2],
    #     "valid_words": ["an", "to", "a"],
    #     "expected": [["a"]],
    # },
    # {
    #     "name": "whole words and alternate segmentations",
    #     "input_digits": [4, 6, 6, 3],
    #     "valid_words": ["home", "good", "hood", "go", "me", "ho"],
    #     "expected": [
    #         ["go", "me"],
    #         ["good"],
    #         ["ho", "me"],
    #         ["home"],
    #         ["hood"],
    #     ],
    # },
    # {
    #     "name": "a valid word may be reused",
    #     "input_digits": [6, 3, 6, 3],
    #     "valid_words": ["me"],
    #     "expected": [["me", "me"]],
    # },
    {
        "name": "prefix can become a word boundary",
        "input_digits": [2, 2, 8],
        "valid_words": ["cat", "at", "a", "act", "bat"],
        "expected": [["a", "at"], ["act"], ["bat"], ["cat"]],
    },
]


import io
import unittest
from contextlib import redirect_stderr, redirect_stdout


def _canonical(combinations):
    """Normalize only the unspecified order of the outer result array."""
    return sorted(tuple(words) for words in combinations)


class SolutionTests(unittest.TestCase):
    def _run_case(self, case):
        console = io.StringIO()

        try:
            with redirect_stdout(console), redirect_stderr(console):
                actual = optimal_solution(
                    list(case["input_digits"]),
                    list(case["valid_words"]),
                )
        finally:
            # The custom result class prints this even if the test fails or the
            # solution raises an exception.
            self._console_output = console.getvalue()

        self.assertEqual(
            _canonical(actual),
            _canonical(case["expected"]),
            f"expected {case['expected']}, but received {actual}",
        )


def _make_test(case):
    def test_case(self):
        self._run_case(case)

    test_case._case_name = case["name"]
    return test_case


# Give unittest one method per case so a failure never prevents later cases
# from running. The numeric prefix also keeps the displayed order stable.
for _number, _case in enumerate(TEST_CASES, start=1):
    _safe_name = "_".join(_case["name"].split()).replace(":", "")
    setattr(
        SolutionTests,
        f"test_{_number:02d}_{_safe_name}",
        _make_test(_case),
    )


class ConsoleTestResult(unittest.TextTestResult):
    """Show captured console output after every individual test result."""

    def getDescription(self, test):
        method = getattr(test, test._testMethodName)
        case_name = getattr(method, "_case_name", None)
        return case_name or super().getDescription(test)

    def _show_console(self, test):
        output = getattr(test, "_console_output", "")
        self.stream.writeln("    console:")

        if output:
            for line in output.rstrip("\n").splitlines():
                self.stream.writeln(f"      {line}")
        else:
            self.stream.writeln("      (no console output)")

        self.stream.flush()

    def addSuccess(self, test):
        super().addSuccess(test)
        self._show_console(test)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._show_console(test)

    def addError(self, test, err):
        super().addError(test, err)
        self._show_console(test)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._show_console(test)


class ConsoleTestRunner(unittest.TextTestRunner):
    resultclass = ConsoleTestResult


if __name__ == "__main__":
    unittest.main(
        verbosity=2,
        failfast=False,
        buffer=False,
        testRunner=ConsoleTestRunner,
    )
