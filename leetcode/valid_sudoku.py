# https://leetcode.com/problems/valid-sudoku/description/

class Solution:
    def isValidSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: bool
        """
        ans = True
        sqs = [[0,1,2],[3,4,5],[6,7,8]]
        for row in range(9):
            for col in range(9):
                val = board[row][col]
                if val == '.':
                    continue
                cur_row = [v for v in board[row] if v != '.']
                cur_col = [board[i][col] for i in range(9) if board[i][col] != '.']
                rowsq, colsq = 0, 0
                for i in range(3):
                    if row in sqs[i]:
                        rowsq = i
                    if col in sqs[i]:
                        colsq = i
                cur_square = [board[r][c] for r in sqs[rowsq] for c in sqs[colsq] if board[r][c] != '.']
                cur_row.remove(val)
                cur_col.remove(val)
                cur_square.remove(val)
                # print("Val: {}, row: {}, col: {}, ans: {}".format(val, row, col, ans))
                # print("cur_row: {}, cur_col: {}, cur_square: {}".format(cur_row, cur_col, cur_square))
                if val not in cur_row and val not in cur_col and val not in cur_square:
                    ans = ans and True
                else:
                    ans = ans and False
        return ans


example1 = [['5', '3', '.', '.', '7', '.', '.', '.', '.'],
            ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
            ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
            ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
            ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
            ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
            ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
            ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
            ['.', '.', '.', '.', '8', '.', '.', '7', '9']]

example2 = [[".","8","7","6","5","4","3","2","1"],
            ["2",".",".",".",".",".",".",".","."],
            ["3",".",".",".",".",".",".",".","."],
            ["4",".",".",".",".",".",".",".","."],
            ["5",".",".",".",".",".",".",".","."],
            ["6",".",".",".",".",".",".",".","."],
            ["7",".",".",".",".",".",".",".","."],
            ["8",".",".",".",".",".",".",".","."],
            ["9",".",".",".",".",".",".",".","."]]

example3 = [[".",".","4",".",".",".","6","3","."],
            [".",".",".",".",".",".",".",".","."],
            ["5",".",".",".",".",".",".","9","."],
            [".",".",".","5","6",".",".",".","."],
            ["4",".","3",".",".",".",".",".","1"],
            [".",".",".","7",".",".",".",".","."],
            [".",".",".","5",".",".",".",".","."],
            [".",".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".",".","."]]

sol = Solution()
print(sol.isValidSudoku(example1))
print(sol.isValidSudoku(example2))
print(sol.isValidSudoku(example3))
