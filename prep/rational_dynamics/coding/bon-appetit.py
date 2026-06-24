# https://www.hackerrank.com/challenges/bon-appetit/problem
import math
import os
import random
import re
import sys

#
# Complete the 'bonAppetit' function below.
#
# The function accepts following parameters:
#  1. INTEGER_ARRAY bill
#  2. INTEGER k
#  3. INTEGER b
#

def bonAppetit(bill, k, b):

    tot = sum(bill)
    subtot = tot - bill[k]

    split = subtot // 2

    if split == b:
        return "Bon Appetit"
    else:
        return b - split

if __name__ == '__main__':
    # first_multiple_input = input().rstrip().split()
    #
    # n = int(first_multiple_input[0])
    #
    # k = int(first_multiple_input[1])
    #
    # bill = list(map(int, input().rstrip().split()))
    #
    # b = int(input().strip())

    assert bonAppetit([3, 10, 2, 9], 1, 12) == 5
    assert bonAppetit([3, 10, 2, 9], 1, 7) == "Bon Appetit"
