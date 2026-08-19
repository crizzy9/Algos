class Solution:
    # DP solution
    def coinChange(self, coins: list[int], amount: int) -> int:
        dp = [float("inf")] * (amount + 1)
        dp[0] = 0

        for coin in coins:
            for x in range(coin, amount + 1):
                dp[x] = min(dp[x], dp[x - coin] + 1)

        return dp[amount] if dp[amount] != float("inf") else -1

    # def coinChangeDfs(self, coins: list[int], amount: int) -> int:
    #     n = len(coins)
    #
    #     def dfs(idx, amount):
    #         if amount == 0:
    #             return 0
    #         if idx < n and amount > 0:
    #             min = float("inf")
    #             for x in range()

    def coinChangeBasic(self, coins: list[int], amount: int) -> int:
        if amount == 0:
            return 0

        minc = 0

        coins.sort(reverse=True)

        for c in coins:
            x, y = divmod(amount, c)

            if x > 0:
                minc += x
                amount = y

            if c == coins[-1] and y > 0:
                # either doesnt work or go back to the next coin
                # needs dp
                return -1

        return minc


if __name__ == "__main__":
    s = Solution()
    assert s.coinChange([1, 2, 5], 11) == 3
    assert s.coinChange([2], 3) == -1
    assert s.coinChange([1], 0) == 0
    print(s.coinChange([186, 419, 83, 408], 6249))
    assert s.coinChange([186, 419, 83, 408], 6249) == 20

    # assert s.coinChangeDfs([1, 2, 5], 11) == 3
    # assert s.coinChangeDfs([2], 3) == -1
    # assert s.coinChangeDfs([1], 0) == 0
    # print(s.coinChangeDfs([186, 419, 83, 408], 6249))
    # assert s.coinChangeDfs([186, 419, 83, 408], 6249) == 20
