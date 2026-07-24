"""
Diagonal Bouncing Robot

You are given a two-dimensional integer matrix and two integers, cellX and cellY, representing the robot’s starting cell.
Coordinates are zero-based: cellX is the row index and cellY is the column index.

The robot follows these rules:

    It begins at (cellX, cellY) and initially moves diagonally in direction (+1, +1).
    The value of the starting cell is included in the total.

    Before each move:
        If the next row coordinate would be outside the matrix, the robot reverses its row direction.
        If the next column coordinate would be outside the matrix, the robot reverses its column direction.
        Both directions may be reversed during the same move.

    After adjusting its direction, the robot moves to the resulting diagonal cell.
    The value of each newly visited cell is added to the total.

    The robot stops when it reaches:
        A corner of the matrix, or
        A cell that it has already visited.

    If the stopping cell was previously visited, its value must not be added again.

A cell is a corner if its row is either the first or last row and its column is either the first or last column.

Return the sum of all cell values collected by the robot.

Example:

matrix = [
    [-12, 33, -4],
    [ 12, -1, 15],
    [ 49, -4, 10]
]

cellX = 0
cellY = 1

Walkthrough

The robot starts at (0, 1):

Position    Value    Running sum
(0, 1)       33          33
(1, 2)       15          48
(2, 1)       -4          44
(1, 0)       12          56

Its movement is as follows:

    From (0, 1), it moves in direction (+1, +1) to (1, 2).
    From (1, 2), continuing in the same direction would cross the right edge. It reverses its column direction and moves to (2, 1).
    From (2, 1), continuing downward would cross the bottom edge. It reverses its row direction and moves to (1, 0).
    From (1, 0), continuing left would cross the left edge. It reverses its column direction and moves to (0, 1).
    Cell (0, 1) was already visited, so the robot stops without adding its value again.

Therefore, the result is:

33 + 15 - 4 + 12 = 56

Output:

56
"""


def robot_path_sum(matrix, cellX, cellY):
    rows, cols = len(matrix), len(matrix[0])

    x, y = cellX, cellY
    dx, dy = 1, 1

    total = matrix[x][y]
    visited = {(x, y)}

    def is_corner(row, col):
        on_top_or_bottom = row == 0 or row == rows - 1
        on_left_or_right = col == 0 or col == cols - 1
        return on_top_or_bottom and on_left_or_right

    if is_corner(x, y):
        return total

    while True:
        if x + dx < 0 or x + dx >= rows:
            dx = -dx

        if y + dy < 0 or y + dy >= cols:
            dy = -dy

        x += dx
        y += dy

        if (x, y) in visited:
            break

        visited.add((x, y))
        total += matrix[x][y]

        if is_corner(x, y):
            break

    return total


matrix = [[-12, 33, -4], [12, -1, 15], [49, -4, 10]]

print(robot_path_sum(matrix, 0, 1))  # 56
