# https://leetcode.com/problems/min-cost-climbing-stairs/

class Solution:
    def minCostClimbingStairs(self, cost):
        # start at 0 or 1
        return min(min_cost(cost), min_cost(cost[1:]))
        

    @staticmethod
    def min_cost(cost):
        if len(cost) <= 2:
            return min(cost[0], cost[1])

        return min(cost[0] + min_cost(cost[1:]), cost[0] + min_cost(cost[2:]))



if __name__ == '__main__':
    sol = Solution()
