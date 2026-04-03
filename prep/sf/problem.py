
import math
import os
import heapq


def minSum(nums: list[int], k: int) -> int:
    # Write your code here
    i = 0
    h = [-num for num in nums]
    heapq.heapify(h)

    while i < k:
        el = heapq.heappop(h)
        heapq.heappush(h, -math.ceil(-el/2))
        i += 1

    f = [-el for el in h]
    return sum(f)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    num_count = int(input().strip())

    num: list[int] = []

    for _ in range(num_count):
        num_item = int(input().strip())
        num.append(num_item)

    k = int(input().strip())

    result = minSum(num, k)

    fptr.write(str(result) + '\n')

    fptr.close()
