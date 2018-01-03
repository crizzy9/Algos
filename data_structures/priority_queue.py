# priority queue using heap
import heapq


class PriorityQueue:

    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        # min heap to get the highest item first by negating priority
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index +=1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def __repr__(self):
        return '{}'.format(self._queue)


class Item:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Item({!r})'.format(self.name)


q = PriorityQueue()
q.push(Item('test1'), 1)
q.push(Item('test2'), 4)
q.push(Item('test3'), 5)
q.push(Item('test4'), 3)
print(q)