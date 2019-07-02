# https://leetcode.com/problems/surrounded-regions/
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        # layer with single item middle if n%2 != 0
        for layer in range(n//2 + n%2 + 1):
            for j in range(n-layer*2-1):
                print("lala")


if __name__ == '__main__':
    sol = Solution()

    board = [[X, X, X, X], [X, O, O, X], [X, X, O, X], [X, O, X, X]]
    res = [[X, X, X, X], [X, X, X, X], [X, X, X, X], [X, O, X, X]]
    sol.solve()
    assert board == res
