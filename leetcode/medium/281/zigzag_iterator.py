class ZigzagIterator:
    def __init__(self, v1: list[int], v2: list[int]):
        self.v1 = v1
        self.v2 = v2
        self.i = 0
        self.j = 0

    def next(self) -> int | None:
        k = None
        if self.i != len(self.v1) and self.j != len(self.v2):
            if self.i < len(self.v1) and self.i <= self.j:
                k = self.v1[self.i]
                self.i += 1
            elif self.j < len(self.v2) and self.j <= self.i:
                k = self.v2[self.j]
                self.j += 1
        elif self.i < len(self.v1):
            k = self.v1[self.i]
            self.i += 1
        else:
            k = self.v2[self.j]
            self.j += 1

        return k

    def hasNext(self) -> bool:
        return self.i < len(self.v1) or self.j < len(self.v2)


# Your ZigzagIterator object will be instantiated and called as such:
# i, v = ZigzagIterator(v1, v2), []
# while i.hasNext(): v.append(i.next())
if __name__ == "__main__":
    i, v = ZigzagIterator([1, 2], [3, 4, 5, 6]), []

    while i.hasNext():
        k = i.next()
        v.append(k)

    assert v == [1, 3, 2, 4, 5, 6]

    i, v = ZigzagIterator([1, 2, 3, 4], [5, 6]), []

    while i.hasNext():
        k = i.next()
        v.append(k)

    assert v == [1, 5, 2, 6, 3, 4]

    i, v = ZigzagIterator([1], []), []

    while i.hasNext():
        v.append(i.next())

    assert v == [1]

    i, v = ZigzagIterator([], [1]), []

    while i.hasNext():
        v.append(i.next())

    assert v == [1]
