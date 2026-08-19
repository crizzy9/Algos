class Solution:
    def gameOfLife(self, board: list[list[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        rows = len(board)
        cols = len(board[0])
        prev = [[board[row][col] for col in range(cols)] for row in range(rows)]
        dirs = [(1, 0), (0, 1), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for i in range(rows):
            for j in range(cols):
                cell = prev[i][j]
                live = 0
                for a, b in dirs:
                    x, y = i + a, j + b
                    if 0 <= x < rows and 0 <= y < cols and prev[x][y] == 1:
                        live += 1

                if cell == 1 and (live < 2 or live > 3):
                    board[i][j] = 0
                if cell == 0 and live == 3:
                    board[i][j] = 1

    def gameOfLifeSpaceEfficient(self, board: list[list[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        rows = len(board)
        cols = len(board[0])
        dirs = [(1, 0), (0, 1), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for i in range(rows):
            for j in range(cols):
                cell = board[i][j]
                live = 0
                for a, b in dirs:
                    x, y = i + a, j + b
                    if 0 <= x < rows and 0 <= y < cols and abs(board[x][y]) == 1:
                        live += 1

                if cell == 1 and (live < 2 or live > 3):
                    board[i][j] = -1
                if cell == 0 and live == 3:
                    board[i][j] = 2

        for i in range(rows):
            for j in range(cols):
                if board[i][j] > 0:
                    board[i][j] = 1
                else:
                    board[i][j] = 0


if __name__ == "__main__":
    s = Solution()
    b = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
    s.gameOfLife(b)
    print(b)
    assert b == [
        [0, 0, 0],
        [1, 0, 1],
        [0, 1, 1],
        [0, 1, 0],
    ]

    b = [[1, 1], [1, 0]]
    s.gameOfLife(b)
    print(b)
    assert b == [[1, 1], [1, 1]]

    b = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
    s.gameOfLifeSpaceEfficient(b)
    print(b)
    assert b == [
        [0, 0, 0],
        [1, 0, 1],
        [0, 1, 1],
        [0, 1, 0],
    ]
