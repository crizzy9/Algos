"""Question 4 — Count alternating-parity subarrays.

Given an integer array ``a``, count its contiguous subarrays in which every pair
of adjacent values has different parity. Every length-one subarray qualifies.

Examples
--------
solution([1, 2, 3, 4]) == 10
solution([1, 3, 2]) == 4
solution([2, 2, 2]) == 3

Guaranteed constraints
-----------------------
1 <= len(a) <= 200_000
-10**9 <= a[i] <= 10**9

A quadratic solution will exceed the time limit on the largest tests.
"""


def solution(a: list[int]) -> int:
    # Write your solution here.

    ans = 0
    rl = 0
    prev_parity = None
    for v in a:
        parity = v % 2

        if prev_parity is not None and prev_parity != parity:
            rl += 1
        else:
            rl = 1

        ans += rl
        prev_parity = parity

    return ans


if __name__ == "__main__":
    assert solution([1, 2, 3, 4]) == 10
    assert solution([1, 3, 2]) == 4
    assert solution([2, 2, 2]) == 3
