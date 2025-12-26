# https://leetcode.com/problems/powx-n/description/
class Solution:
    def myPow(self, x, n):
        """
        :type x: float
        :type n: int
        :rtype: float
        """
        if n < 0:
            x = 1/x
            n = abs(n)
        res = 1
        cp = x
        i = n
        while i > 0:
            if (i % 2) == 1:
                res = res * cp
            cp = cp * cp
            i = i//2
        return res


sol = Solution()
print(sol.myPow(2.1462, 5))
print(sol.myPow(0.00001, 2147483647))