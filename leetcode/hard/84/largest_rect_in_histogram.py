
from typing import List

class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        stack = [-1]
        max_area = 0
        for i in range(len(heights)):
            while stack[-1] != -1 and heights[stack[-1]] >= heights[i]:
                h = heights[stack.pop()]
                w = i - stack[-1] - 1
                max_area = max(max_area, h*w)
            stack.append(i)

        while stack[-1] != -1:
            h = heights[stack.pop()]
            w = len(heights) - stack[-1] - 1
            max_area = max(max_area, h*w)
        return max_area

if __name__ == '__main__':
    sol = Solution()

    s1 = sol.largestRectangleArea([2,1,5])
    print(f"s1: {s1}")
    assert s1 == 10

    s1 = sol.largestRectangleArea([2,1,5,6,2,3])
    print(f"s1: {s1}")
    assert s1 == 10

    s2 = sol.largestRectangleArea([6,7,5,2,4,5,9,3])
    print(f"s2: {s2}")
    assert s2 == 16
