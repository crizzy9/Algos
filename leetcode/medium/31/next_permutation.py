from typing import List

class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        i = len(nums) - 2
        while i >= 0 and nums[i+1] <= nums[i]:
            i -= 1

        if i >= 0:
            j = len(nums) - 1
            while nums[j] <= nums[i]:
                j -= 1
            self.swap(nums, i, j)

        self.reverse(nums, i+1)

    def reverse(self, nums, start):
        i, j = start, len(nums) - 1
        while i < j:
            self.swap(nums, i, j)
            i += 1
            j -= 1

    def swap(self, nums, i, j):
        temp = nums[i]
        nums[i] = nums[j]
        nums[j] = temp


if __name__ == "__main__":
    s = Solution()

    nums = [1,2,3]
    s.nextPermutation(nums)
    assert nums == [1,3,2]

    nums = [1,3,2]
    s.nextPermutation(nums)
    assert nums == [2,1,3]

    nums = [3,2,1]
    s.nextPermutation(nums)
    assert nums == [1,2,3]

    nums = [1,4,5,2,9]
    s.nextPermutation(nums)
    assert nums == [1,4,5,9,2]

    nums = [1,4,5,9,2]
    s.nextPermutation(nums)
    assert nums == [1,4,9,2,5]

    nums = [1,5,8,4,7,6,5,3,1]
    s.nextPermutation(nums)
    assert nums == [1,5,8,5,1,3,4,6,7]

