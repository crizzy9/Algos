from collections import OrderedDict


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity: int = capacity
        self.q: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.q:
            return -1
        self.q.move_to_end(key)
        return self.q[key]

    def put(self, key: int, value: int) -> None:
        if key in self.q:
            self.q.move_to_end(key)

        self.q[key] = value

        if len(self.q) > self.capacity:
            _ = self.q.popitem(False)

if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put(1,1)
    cache.put(2,2)
    assert cache.get(1) == 1
    cache.put(3,3)
    assert cache.get(2) == -1
    cache.put(4,4)
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4
