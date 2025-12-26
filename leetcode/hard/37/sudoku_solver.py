# https://leetcode.com/problems/sudoku-solver/description/
import pprint
import copy
class Solution:

    def __init__(self):
        self.sqs = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.possibilities = {}

    def solveSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """
        # calculating possibilities
        for row in range(9):
            for col in range(9):
                val = board[row][col]
                if val != '.':
                    continue
                cur_row = [v for v in board[row] if v != '.']
                cur_col = [board[i][col] for i in range(9) if board[i][col] != '.']
                rowsq, colsq = self.get_square(row, col)
                cur_square = [board[r][c] for r in self.sqs[rowsq] for c in self.sqs[colsq] if board[r][c] != '.']
                union = set(cur_row).union(cur_col).union(cur_square)
                sym_diff = union.symmetric_difference([str(i) for i in range(1, 10)])
                self.possibilities[(row, col)] = sym_diff
        pp = pprint.PrettyPrinter(indent=4)
        print("Initial:")
        pp.pprint(board)

        # acts as a stack
        guesses = []
        backtrack = {}
        while self.possibilities:
            prev_pos = dict(self.possibilities)

            for position, vals in list(self.possibilities.items()):
                row = position[0]
                col = position[1]
                # updating board for places where only 1 value is possible
                if len(vals) == 1:
                    # resolving value in board
                    del self.possibilities[position]
                    board[row][col] = vals.pop()
                    self.update_possibilities(board[row][col], row, col)
                    continue

                # updating board where number is possible only in one place in the square
                rowsq, colsq = self.get_square(row, col)
                ps = set()
                for r in self.sqs[rowsq]:
                    for c in self.sqs[colsq]:
                        if self.possibilities.get((r, c)) and (r, c) != position:
                            ps = ps.union(self.possibilities[(r, c)])
                diff = self.possibilities[position].difference(ps)
                if len(diff) == 1:
                    self.possibilities[position] = diff
                # backtracking
                if not self.possibilities[position]:
                    incorrect_guess = guesses.pop()
                    # print("Incorrect guess... Backtracking! guess:", incorrect_guess)
                    self.possibilities = backtrack[incorrect_guess][0]
                    board = backtrack[incorrect_guess][1]
                    del backtrack[incorrect_guess]
                    break

            # if no further change in possibilities is possible try guessing
            if self.possibilities == prev_pos:
                # print("Making a guess...")
                pos = min(self.possibilities, key=lambda k: len(self.possibilities[k]))
                current_guess = self.possibilities[pos].pop()
                guesses.append(pos)
                backtrack[pos] = (copy.deepcopy(self.possibilities), copy.deepcopy(board))
                self.possibilities[pos] = set(current_guess)

        print("\n"*2+"Solved:")
        pp.pprint(board)

    def update_possibilities(self, val, row, col):
        # update possibilities for cur square and cur col and cur row
        rowsq, colsq = self.get_square(row, col)
        for r in self.sqs[rowsq]:
            for c in self.sqs[colsq]:
                if self.possibilities.get((r, c)) and val in self.possibilities[(r, c)]:
                    self.possibilities[(r, c)].remove(val)
        for i in range(9):
            if self.possibilities.get((row, i)) and val in self.possibilities[(row, i)]:
                self.possibilities[(row, i)].remove(val)
            if self.possibilities.get((i, col)) and val in self.possibilities[(i, col)]:
                self.possibilities[(i, col)].remove(val)

    def get_square(self, row, col):
        rowsq, colsq = 0, 0
        for i in range(3):
            if row in self.sqs[i]:
                rowsq = i
            if col in self.sqs[i]:
                colsq = i
        return rowsq, colsq


# easy
example1 = [['5', '3', '.', '.', '7', '.', '.', '.', '.'],
            ['6', '.', '.', '1', '9', '5', '.', '.', '.'],
            ['.', '9', '8', '.', '.', '.', '.', '6', '.'],
            ['8', '.', '.', '.', '6', '.', '.', '.', '3'],
            ['4', '.', '.', '8', '.', '3', '.', '.', '1'],
            ['7', '.', '.', '.', '2', '.', '.', '.', '6'],
            ['.', '6', '.', '.', '.', '.', '2', '8', '.'],
            ['.', '.', '.', '4', '1', '9', '.', '.', '5'],
            ['.', '.', '.', '.', '8', '.', '.', '7', '9']]

# medium
example2 = [['8', '.', '.', '.', '.', '.', '.', '.', '7'],
            ['.', '.', '4', '.', '8', '.', '.', '9', '.'],
            ['.', '1', '6', '.', '.', '5', '2', '.', '.'],
            ['.', '.', '.', '.', '.', '2', '8', '.', '.'],
            ['.', '2', '.', '.', '5', '.', '.', '1', '.'],
            ['.', '.', '3', '4', '.', '.', '.', '.', '.'],
            ['.', '.', '7', '3', '.', '.', '5', '6', '.'],
            ['.', '5', '.', '.', '2', '.', '3', '.', '.'],
            ['6', '.', '.', '.', '.', '.', '.', '.', '4']]

# hardest
example3 = [['8', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '3', '6', '.', '.', '.', '.', '.'],
            ['.', '7', '.', '.', '9', '.', '2', '.', '.'],
            ['.', '5', '.', '.', '.', '7', '.', '.', '.'],
            ['.', '.', '.', '.', '4', '5', '7', '.', '.'],
            ['.', '.', '.', '1', '.', '.', '.', '3', '.'],
            ['.', '.', '1', '.', '.', '.', '.', '6', '8'],
            ['.', '.', '8', '5', '.', '.', '.', '1', '.'],
            ['.', '9', '.', '.', '.', '.', '4', '.', '.']]

example4 = [[".", ".", "9", "7", "4", "8", ".", ".", "."],
            ["7", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "2", ".", "1", ".", "9", ".", ".", "."],
            [".", ".", "7", ".", ".", ".", "2", "4", "."],
            [".", "6", "4", ".", "1", ".", "5", "9", "."],
            [".", "9", "8", ".", ".", ".", "3", ".", "."],
            [".", ".", ".", "8", ".", "3", ".", "2", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "6"],
            [".", ".", ".", "2", "7", "5", "9", ".", "."]]


sol = Solution()
print("EXAMPLE 1: ")
sol.solveSudoku(example1)
print("EXAMPLE 2: ")
sol.solveSudoku(example2)
print("EXAMPLE 3: ")
sol.solveSudoku(example3)
print("EXAMPLE 4: ")
sol.solveSudoku(example4)
