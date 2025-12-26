from collections import Counter


class Solution:
    def combinationSum(self, candidates, target):
        """
        :type candidates: List[int]
        :type target: int
        :rtype: List[List[int]]
        """

        sorted_candidates = sorted(candidates)
        combs = []
        self.go_through(sorted_candidates, target, [], len(sorted_candidates) - 1, combs)
        return combs

    def go_through(self, candidates, target, counted, from_to_left, combinations):
        if target == 0:
            combinations.append(counted)
        else:
            for i in range(from_to_left, -1, -1):
                if candidates[i] <= target:
                    new_counted = counted[:]
                    new_counted.append(candidates[i])
                    self.go_through(candidates, target - candidates[i], new_counted, i, combinations)


cs = [2, 3, 6, 7]
t = 7
sol = Solution()
print(sol.combinationSum(cs, t))
print(sol.combinationSum([1, 10, 2, 3, 4, 5, 6, 7, 8, 9], 9))
