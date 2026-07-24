class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        self.rows = len(board)
        self.cols = len(board[0])
        self.board = board

        for row in range(rows):
            for col in range(cols):
                if self.backtrack(row, col, word):
                    return True

        return False

    def backtrack(self, row, col, suffix):
        if len(suffix) == 0:
            return True

        if (
            row < 0
            or col < 0
            or row >= self.rows
            or col >= self.cols
            or suffix[0] != self.board[row][col]
        ):
            return False

        ans = False

        self.board[row][col] = "#"
        for rowOffset, colOffset in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ans = self.backtrack(row + rowOffset, col + colOffset, suffix[1:])
            if ans:
                break

        self.board[row][col] = suffix[0]

        return ans


if __name__ == "__main__":
    s = Solution()
    assert s.exist(
        [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCCED"
    )
    assert s.exist(
        [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "SEE"
    )
    assert not s.exist(
        [["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCB"
    )
