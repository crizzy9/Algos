"""Question 3 — Bubble-board simulation.

``bubbles`` is a rectangular matrix. A positive integer represents a bubble's
color, and 0 represents an empty cell. ``operations`` contains clicks in the
form ``[row, column]``.

Process the clicks in order:

1. If the clicked cell is empty, do nothing.
2. Otherwise, remove the clicked bubble and every *immediate diagonal neighbor*
   of the same color. The four possible diagonal offsets are (-1, -1), (-1, 1),
   (1, -1), and (1, 1). This step is not recursive.
3. Apply gravity independently to every column: nonzero values retain their
   relative order and fall toward the bottom; empty cells move to the top.

Return the board after every operation has been processed. You may mutate and
return the input matrix.

Example
-------
For

    bubbles = [
        [1, 2, 1],
        [2, 1, 2],
        [1, 2, 1],
    ]
    operations = [[1, 1]]

the output is

    [
        [0, 0, 0],
        [0, 2, 0],
        [2, 2, 2],
    ]

Guaranteed constraints
-----------------------
1 <= rows, columns <= 50
0 <= bubbles[row][column] <= 10**9
0 <= len(operations) <= 500
Every click is inside the board.
"""


def solution(bubbles: list[list[int]], operations: list[list[int]]) -> list[list[int]]:
    # Write your solution here.
    nrows = len(bubbles)
    ncols = len(bubbles[0])

    for o in operations:
        x, y = o
        c = bubbles[x][y]

        if c == 0:
            continue

        diags = [(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)]
        to_remove = [(x, y)]
        for d in diags:
            if (0 <= d[0] < nrows) and (0 <= d[0] < ncols) and bubbles[d[0]][d[1]] == c:
                to_remove.append((d[0], d[1]))

        for rr, rc in to_remove:
            bubbles[rr][rc] = 0

        # apply gravity
        for j in range(ncols):
            values = [bubbles[i][j] for i in range(nrows) if bubbles[i][j] != 0]
            empty_count = nrows - len(values)
            for i, v in enumerate([0] * empty_count + values):
                bubbles[i][j] = v

    return bubbles


if __name__ == "__main__":
    bubbles = [
        [1, 2, 1],
        [2, 1, 2],
        [1, 2, 1],
    ]
    operations = [[1, 1]]

    assert solution(bubbles, operations) == [[0, 0, 0], [0, 2, 0], [2, 2, 2]]
