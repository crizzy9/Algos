from typing import List

class Solution:
    def empty_board(self, n):
        board = []
        for _ in range(n):
            board.append("."*n)

    def get_positions(self, board, n, col):
        board[0][col] = "Q"
        for i in range(1, n):
            board[i]


    def valid_position(self, position):
        pass

    def solveNQueens(self, n: int) -> List[List[str]]:
        positions = []
        for i in range(n):
            board = self.empty_board(n)
            pos = self.get_positions(board, n, i)
            if self.valid_position(pos):
                positions.append(pos)

        return positions


if __name__ == '__main__':
    sol = Solution()
    res = sol.solveNQueens(4)
    print(res)
    assert len(res) == 2


# sonal bday
# studs solittare diamond earrings. natural not labgrown
# cartier panther ring
# dior bag
