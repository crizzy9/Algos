class Node:
    def __init__(self, value=None, pointer=None):
        self.value = value
        self.pointer = pointer


class LinkedStack:
    def __init__(self):
        self.head = None

    def isEmpty(self):
        return not bool(self.head)

    def push(self, item):
        self.head = Node(item, self.head)

    def pop(self):
        if self.head:
            node = self.head
            self.head = node.pointer
            return node.value
        else:
            print('Stack is empty')

    def size(self):
        node = self.head
        count = 0
        while node:
            count += 1
            node = node.pointer

    def _printList(self):
        node = self.head
        while node:
            print(node.value)
            node = node.pointer


if __name__ == '__main__':
    stack = LinkedStack()
    for i in range(15,20):
        stack.push(i)
    print("Stack:")
    stack._printList()
    for i in range(10, 5, -1):
        stack.push(i)
    print("Stack:")
    stack._printList()
    for i in range(1, 13):
        stack.pop()
    print("Stack:")
    stack._printList()


    stack.push(25)
    stack.push(3)
    stack.push(11)
    stack.push(31)
    stack.push(29)
    print("Stack:")
    print(stack._printList())
