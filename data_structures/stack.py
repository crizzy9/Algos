# class implementation for Stack
class Stack:

    def __init__(self):
        self.content = []
        self.min_array = []
        self.min = float('inf')

    def push(self, value):
        if value < self.min:
            self.min = value
        self.content.append(value)
        # no dupicates
        if self.min not in self.min_array:
            self.min_array.append(self.min)

    def pop(self):
        if self.content:
            value = self.content.pop()
            if value == self.min:
                self.min_array.pop()
            if self.min_array:
                self.min = self.min_array[-1]
            return value
        else:
            return 'Stack is empty'

    def find_min(self):
        if self.min_array:
            return self.min
        else:
            return 'No min value for Empty Stack'

    def size(self):
        return len(self.content)

    def isEmpty(self):
        return not bool(self.content)

    def peek(self):
        if self.content:
            return self.content[-1]
        else:
            return 'Stack is empty'

    def __repr__(self):
        return '{}'.format(self.content)


if __name__ == '__main__':
    stack = Stack()
    for i in range(15,20):
        stack.push(i)
    print("Stack:", stack)
    print(stack.min_array)
    for i in range(10, 5, -1):
        stack.push(i)
    print("Stack:", stack)
    print(stack.min_array)
    for i in range(1, 13):
        print(stack.pop(), stack.find_min())
    print("Stack:", stack)
    print(stack.min_array)


    # simple implementation using only list
    stk = []
    # push
    stk.append(15)
    stk.append(30)
    # popping last element in list
    stk.pop()

    stack.push(25)
    stack.push(3)
    stack.push(11)
    stack.push(31)
    stack.push(29)
    print("Stack:", stack.__repr__())
    print(stack.min_array)
