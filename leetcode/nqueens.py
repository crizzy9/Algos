class Solution:

    def solveNQueens(self, n: int) -> List[List[str]]:
        results = []
        board = []
        for i in range(n):
            board.append([])
            for j in range(n):
                board[i].append('.')

        positions = []
        for i in range(n):
            get_positions(board, i)

        return results

    def get_positions(self, board, col):
        if col == 0:
            return [(i, 0) for i in range(1, len(board)-1)]
        else:



    def clear_board(self, board):
        for i in range(len(board)):
            for j in range(len(board)):
                board[i][j] = '.'
        return board

    def join_board(self, board):
        return [''.join(board[i]) for i in range(len(board))]


if __name__ == '__main__':
    sol = Solution()
    res = sol.solveNQueens(4)
    assert len(res) == 2
