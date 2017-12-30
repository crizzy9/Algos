class Queue:
    def __init__(self):
        self.in_stack = []
        self.out_stack = []

    def _transfer(self):
        while self.in_stack:
            self.out_stack.append(self.in_stack.pop())

    def enqueue(self, item):
        self.in_stack.append(item)

    def dequeue(self):
        if not self.out_stack:
            self._transfer()
        if self.out_stack:
            return self.out_stack.pop()
        else:
            return "Queue empty!"

    def size(self):
        return len(self.in_stack) + len(self.out_stack)

    def peek(self):
        if not self.out_stack:
            self._transfer()
        if self.out_stack:
            return self.out_stack[-1]
        else:
            return "Queue empty!"

    def __repr__(self):
        if not self.out_stack:
            self._transfer()
        if self.out_stack:
            return '{}'.format(self.out_stack)
        else:
            return "Queue empty!"

    def isEmpty(self):
        return not (bool(self.in_stack) or bool(self.out_stack))


if __name__ == '__main__':
    q = Queue()
    print("Is the queue empty? ", q.isEmpty())
    print("Adding 0 to 10 in the queue...")
    for i in range(10):
        q.enqueue(i)

    print("Queue size: ", q.size())
    print("Queue peek : ", q.peek())
    print("Dequeue...", q.dequeue())
    print("Queue peek: ", q.peek())
    print("Is the queue empty? ", q.isEmpty())
    print("Printing the queue...")
    print(q)