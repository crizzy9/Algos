class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return not bool(self.items)

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[-1]

    def __repr__(self):
        return "{}".format(self.items)


if __name__ == "__main__":
    q = Queue()
    q.enqueue(5)
    q.enqueue(7)
    q.enqueue(25)
    q.enqueue(3)
    q.enqueue(15)
    print(q)
    q.dequeue()
    print(q)
    q.dequeue()
    print(q)