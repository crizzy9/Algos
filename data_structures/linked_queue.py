class Node:
    def __init__(self, value=None, pointer=None):
        self.value = value
        self.pointer = pointer


class LinkedQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def isEmpty(self):
        return not bool(self.head)

    def enqueue(self, value):
        node = Node(value)
        if not self.head:
            self.head = node
            self.tail = node
        else:
            if self.tail:
                self.tail.pointer = node
            self.tail = node

    def dequeue(self):
        if self.head:
            value = self.head.value
            self.head = self.head.pointer
            return value
        else:
            print("Queue is empty, cannot dequeue")

    def size(self):
        node = self.head
        count = 0
        while node:
            count +=1
            node = node.pointer
        return count

    def peek(self):
        return self.head.value

    def _print(self):
        node = self.head
        while node:
            print(node.value)
            node = node.pointer


if __name__ == "__main__":
    q = LinkedQueue()
    for i in range(10):
        q.enqueue(i)
    q._print()
    q.dequeue()
    q.dequeue()
    print()
    q._print()
