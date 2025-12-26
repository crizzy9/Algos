from typing import List

class Solution:
    def empty_board(self, n):
        board = []
        for _ in range(n):
            board.append("."*n)

    def get_positions(self, board, col):
        if col == 0:
            return [(i, 0) for i in range(1, len(board)-1)]
        else:
            return []

    def solveNQueens(self, n: int) -> List[List[str]]:
        results = []
        board = self.empty_board(n)
        positions = []
        for i in range(n):
            positions.append(self.get_positions(board, i))

        return results


if __name__ == '__main__':
    sol = Solution()
    res = sol.solveNQueens(4)
    print(res)
    assert len(res) == 2
