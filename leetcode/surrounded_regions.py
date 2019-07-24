# https://leetcode.com/problems/surrounded-regions/
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        # layer with single item middle if n%2 != 0
        # for layer in range(n//2 + n%2 + 1):
        #     for j in range(n-layer*2-1):
        #         print("lala")

        n = len(board)
        zeros = set()
        for i in range(n-1):
            if board[0][i] == 'O':
                zeros.add((0,i))
            if board[i][n-1] == 'O':
                zeros.add((i, n-1))
            if board[n-1][n-i-1] == 'O':
                zeros.add((n-1, n-i-1))
            if board[n-i-1][n-1] == 'O':
                zeros.add((n-i-1, n-1))

        c = 0
        while c < len(zeros):
            i, j == zeros[0]


if __name__ == '__main__':
    sol = Solution()

    board = [[X, X, X, X], [X, O, O, X], [X, X, O, X], [X, O, X, X]]
    res = [[X, X, X, X], [X, X, X, X], [X, X, X, X], [X, O, X, X]]
    sol.solve()
    assert board == res
