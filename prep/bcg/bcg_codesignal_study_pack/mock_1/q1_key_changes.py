"""Question 1 — Case-insensitive key changes.

You are given a string ``key_sequence`` containing English letters. Two letters
refer to the same keyboard key when they differ only by case.

Count the indices ``i`` (1 <= i < len(key_sequence)) at which the key used for
``key_sequence[i]`` differs from the key used for ``key_sequence[i - 1]``.

Examples
--------
solution("aAbBcC") == 2
solution("AaAa") == 0
solution("CodeSignal") == 9

Guaranteed constraints
-----------------------
1 <= len(key_sequence) <= 100_000
key_sequence contains only a-z and A-Z.
"""


def solution(key_sequence: str) -> int:
    # Write your solution here.
    seq = key_sequence.lower()

    r = 0
    for i in range(1, len(seq)):
        if seq[i] != seq[i - 1]:
            r += 1
    return r


if __name__ == "__main__":
    assert solution("aAbBcC") == 2
    assert solution("AaAa") == 0
    assert solution("CodeSignal") == 9
