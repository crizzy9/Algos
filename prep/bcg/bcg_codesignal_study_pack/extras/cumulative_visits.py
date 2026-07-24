"""Additional reported problem — Cumulative website visits.

``visits[i]`` is the number of visits received on day ``i``. Return the smallest
index ``i`` for which ``visits[0] + ... + visits[i]`` is at least ``target``.
Return -1 if the cumulative total never reaches the target.

Examples
--------
solution([100, 200, 150, 400], 450) == 2
solution([5, 5], 11) == -1

Guaranteed constraints
-----------------------
1 <= len(visits) <= 100_000
0 <= visits[i] <= 10**9
1 <= target <= 10**18
"""


def solution(visits: list[int], target: int) -> int:
    # Write your solution here.
    s = 0
    ans = -1
    for i in range(len(visits)):
        s += visits[i]
        if s >= target:
            ans = i
            break
    return ans


if __name__ == "__main__":
    assert solution([100, 200, 150, 400], 450) == 2
    assert solution([5, 5], 11) == -1
