# https://leetcode.com/problems/find-all-duplicates-in-an-array/
from collections import Counter

class Solution:
    def findDuplicates(self, nums):
        c = Counter(nums)
        return list(filter(lambda x: c[x] == 2, c.keys()))

    def findDuplicates2(self, nums):
        s = set()
        output = []
        for num in nums:
            if num not in s:
                s.add(num)
            else:
                output.append(num)
        return output

    def findDuplicates3(self, nums):
        mask = 0
        ans = []
        for num in nums:
            print("num", num)
            print("1<<num", (1<<num))
            print("mask", mask)
            print("mask|(1<<num)", mask|(1<<num))
            print("mask&(1<<num)", mask & (1 << num))
            if mask & (1 << num):
                ans.append(num)
            else:
                mask |= (1 << num)
        return ans

if __name__ == '__main__':
    sol = Solution()
    res = sol.findDuplicates([4,3,2,7,8,2,3,1])
    assert set(res) == set([2,3])

    res = sol.findDuplicates3([4,3,2,7,8,2,3,1])
    assert set(res) == set([2,3])
