class Solution:
    def combine(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: List[List[int]]
        """
        return self.combinations(1, n+1, k)

    def combinations(self, start, end, k):
        if k == 1:
            ans = [[i] for i in range(start, end)]
            return ans
        else:
            ans = []
            for i in range(start, end + 1):
                for comb in self.combinations(i + 1, end, k - 1):
                    ans.append([i]+comb)
            return ans

sol = Solution()

print(sol.combine(4, 2))
