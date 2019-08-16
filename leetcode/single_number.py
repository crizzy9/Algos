# https://leetcode.com/problems/single-number/
class Solution:
    def singleNumber(self, nums):
        # xor:
        # a xor 0 = a
        # a xor a = 0
        # a xor b xor a = b
        # xor all of them together to eliminate duplicates
        a = 0
        for n in nums:
            a ^= n
        return a


if __name__ == '__main__':
    sol = Solution()
    assert sol.singleNumber([2,2,1]) == 1
    assert sol.singleNumber([4,2,1,1,2]) == 4
    assert sol.singleNumber([5,67,2,4,67,4,1,1,5,7,2]) == 7
    assert sol.singleNumber([54,1,6,32,1,6,32,3,54]) == 3

