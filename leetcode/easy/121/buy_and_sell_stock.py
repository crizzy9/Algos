class Solution:
    # Time Complexity:  O(n^2)
    # Space Complexity: O(1)
    # Result: Time Limit Exceeded
    def maxProfitBruteForce(self, prices: list[int]) -> int:
        n = len(prices)
        max_diff = 0
        for i in range(n - 1):
            for j in range(i, n):
                diff = prices[j] - prices[i]
                max_diff = max(max_diff, diff)

        return max_diff

    # Time Complexity:  O(n)
    # Space Complexity: O(1)
    # Result: Accepted
    def maxProfit(self, prices: list[int]) -> int:
        min_price = float("inf")
        max_profit = 0

        for i in range(len(prices)):
            if prices[i] < min_price:
                min_price = prices[i]
            elif prices[i] - min_price > max_profit:
                max_profit = prices[i] - min_price

        return int(max_profit)


if __name__ == "__main__":
    s = Solution()
    assert s.maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0
