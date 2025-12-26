# Kth smallest element in a row-wise and column-wise sorted 2D array | Set 1
#
# Given an n x n matrix, where every row and column is sorted in non-decreasing order. Find the kth smallest element in the given 2D array.
#
# For example, consider the following 2D array.
#
# 10, 20, 30, 40
# 15, 25, 35, 45
# 24, 29, 37, 48
# 32, 33, 39, 50
# The 3rd smallest element is 20 and 7th smallest element is 30

# check diagonal elements
from typing import List

class Solution:
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        sorted_arr = sorted([el for sl in matrix for el in sl])
        print(sorted_arr)
        return sorted_arr[k-1]

    def kthSmallest2(self, matrix: List[List[int]], k: int) -> int:
        sorted_arr = []
        i = 0
        while i < len(matrix):
            sorted_arr.extend(sorted([matrix[i-k][k] for k in range(i+1)]))
            i += 1
        print(sorted_arr)
        return sorted_arr[k-1]

if __name__ == "__main__":
    s = Solution()

    a = [
        [10, 20, 30, 40],
        [15, 25, 35, 45],
        [24, 29, 37, 48],
        [32, 33, 39, 50]
    ]
    print(s.kthSmallest(a,3))

    a = [[1,5,9],[10,11,13],[12,13,15]]
    print(s.kthSmallest(a,8))
