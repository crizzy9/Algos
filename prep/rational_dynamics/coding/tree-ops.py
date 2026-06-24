class Node:
    def __init__(self, info):
        self.info = info
        self.left = None
        self.right = None
        self.level = None

    def __str__(self):
        return str(self.info)


def preOrder(root):
    if root == None:
        return
    print(root.info, end=" ")
    preOrder(root.left)
    preOrder(root.right)


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            curr = self.root
            while True:
                if val < curr.info:
                    if curr.left:
                        curr = curr.left
                    else:
                        curr.left = Node(val)
                        break
                elif val > curr.info:
                    if curr.right:
                        curr = curr.right
                    else:
                        curr.right = Node(val)
                        break
                else:
                    break


tree = BinarySearchTree()
t = int(input())

arr = list(map(int, input().split()))

for i in range(t):
    tree.insert(arr[i])

preOrder(tree.root)
