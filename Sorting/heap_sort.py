import heapq
import random

arr1000 = [random.randint(0, 1000) for _ in range(1000)]
arr10000 = [random.randint(0, 10000) for _ in range(10000)]

heapq.heapify(arr1000)
heapq.heapify(arr10000)
print([heapq.heappop(arr1000) for _ in range(len(arr1000))])
print([heapq.heappop(arr10000) for _ in range(len(arr10000))])