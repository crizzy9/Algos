# https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/
class Solution:
    def findDisappearedNumbers(self, nums):
        mask = 0
        res = []
        for num in nums:
            if not mask & (1 << num):
                mask |= (1 << num)

        for i in range(len(nums)):
            if not mask & (1 << i+1):
                res.append(i+1)

        return res



if __name__ == '__main__':
    sol = Solution()
    res = sol.findDisappearedNumbers([4,3,2,7,8,2,3,1])
    assert res == [5,6]


