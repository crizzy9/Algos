# https://www.hackerrank.com/challenges/sock-merchant/problem

import math
import os
import random
import re
import sys

#
# Complete the 'sockMerchant' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. INTEGER_ARRAY ar
#

def sockMerchant(n, ar):
    m = {}

    for i in range(n):
        m[ar[i]] = m.get(ar[i], 0) + 1

    np = len([k for k,v in m.items() if v%2 != 0])

    return (n - np) // 2

if __name__ == '__main__':
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')
    #
    # n = int(input().strip())
    #
    # ar = list(map(int, input().rstrip().split()))
    #
    # result = sockMerchant(n, ar)
    #
    # fptr.write(str(result) + '\n')
    #
    # fptr.close()

    assert sockMerchant(9, [10, 20, 20, 10, 10, 30, 50, 10, 20]) == 3
    assert sockMerchant(10, [1, 1, 3, 1, 2, 1, 3, 3, 3, 3]) == 4
