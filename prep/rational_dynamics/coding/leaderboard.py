# https://www.hackerrank.com/challenges/climbing-the-leaderboard/problem

import math
import os
import random
import re
import sys
from bisect import bisect_right

#
# Complete the 'climbingLeaderboard' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER_ARRAY ranked
#  2. INTEGER_ARRAY player
#

def climbingLeaderboard(ranked, player):
    ranks = sorted(set(ranked))

    prs = []
    n = len(ranks)
    for p in player:
        for i in range(n):
            r = ranks[i]
            if p < r:
                prs.append(n-i+1)
                break
            elif p == r:
                prs.append(n-i)
                break
            elif i == n-1 and p > r:
                prs.append(1)
                break

    return prs

def climbingLeaderboardSearch(ranked, player):
    ranks = sorted(set(ranked))

    prs = []
    n = len(ranks)
    for p in player:
        loc = bisect_right(ranks, p)
        prs.append(n-loc+1)

    return prs

if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')
    #
    # ranked_count = int(input().strip())
    #
    # ranked = list(map(int, input().rstrip().split()))
    #
    # player_count = int(input().strip())
    #
    # player = list(map(int, input().rstrip().split()))
    #
    # result = climbingLeaderboard(ranked, player)
    #
    # fptr.write('\n'.join(map(str, result)))
    # fptr.write('\n')
    #
    # fptr.close()
    # assert climbingLeaderboard([100,100,50,40,40,20,10], [5,25,50,120]) == [6,4,2,1]
    assert climbingLeaderboardSearch([100,100,50,40,40,20,10], [5,25,50,120]) == [6,4,2,1]
