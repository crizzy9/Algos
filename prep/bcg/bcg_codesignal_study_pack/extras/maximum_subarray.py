"""Additional reported problem — Maximum contiguous-subarray sum.

Given a nonempty integer array ``numbers``, return the greatest possible sum of
a nonempty contiguous subarray.

Examples
--------
solution([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
solution([-8, -3, -6]) == -3

Guaranteed constraints
-----------------------
1 <= len(numbers) <= 200_000
-10**9 <= numbers[i] <= 10**9

A quadratic solution will exceed the time limit on the largest tests.
"""


def solution(numbers: list[int]) -> int:
    # Write your solution here.
    end = best = numbers[0]
    for v in numbers[1:]:
        end = max(v, end + v)
        best = max(best, end)
    return best


if __name__ == "__main__":
    assert solution([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert solution([-8, -3, -6]) == -3
