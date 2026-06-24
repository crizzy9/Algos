# https://www.hackerrank.com/challenges/magic-square-forming/problem

import math
import os
import random
import re
import sys

#
# Complete the 'formingMagicSquare' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY s as parameter.
#

def formingMagicSquare(s):
    # calculate all 8 sums
    magic = [[8, 1, 6, 3, 5, 7, 4, 9, 2], [6, 1, 8, 7, 5, 3, 2, 9, 4],
            [4, 3, 8, 9, 5, 1, 2, 7, 6], [2, 7, 6, 9, 5, 1, 4, 3, 8],
            [2, 9, 4, 7, 5, 3, 6, 1, 8], [4, 9, 2, 3, 5, 7, 8, 1, 6],
            [6, 7, 2, 1, 5, 9, 8, 3, 4], [8, 3, 4, 1, 5, 9, 6, 7, 2]]

    sx = s[0]+s[1]+s[2]
    mini = 2**64 # INT MAX

    for m in magic:
        d = 0
        for i,j in zip(sx, m):
            d += abs(i-j)
        mini = min(d, mini)

    return mini

if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')
    #
    # s = []
    #
    # for _ in range(3):
    #     s.append(list(map(int, input().rstrip().split())))
    #
    # result = formingMagicSquare(s)
    #
    # fptr.write(str(result) + '\n')
    #
    # fptr.close()

    assert formingMagicSquare([[4,9,2], [3,5,7], [8,1,5]]) == 1
    assert formingMagicSquare([[4,8,2], [4,5,7], [6,1,6]]) == 4
