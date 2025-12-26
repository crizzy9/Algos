
from typing import List

class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        pairs = set()

        return list(pairs)

if __name__ == '__main__':
    sol = Solution()

    s1 = sol.fourSum([1,0,-1,0,-2,2], 0)
    print(f"s1: {s1}")
    assert s1 == [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
