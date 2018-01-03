import heapq

l = [4,6,8,1]
# will convert l into min heap in place
heapq.heapify(l)
# heaps arent ordered in any particular order except for the first element which is either min or max
print(l)

h = []
heapq.heappush(h, (4, 'study'))
heapq.heappush(h, (2, 'have fun'))
heapq.heappush(h, (1, 'food'))
heapq.heappush(h, (3, 'work'))
print(h)


heapq._heapify_max(l)
print(l)
print(heapq._heappop_max(l))
# get n largest element in using heap
print(heapq.nlargest(3, l))
