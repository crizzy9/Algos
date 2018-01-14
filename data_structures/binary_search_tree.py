class Node:
    def __init__(self, key):
        self.val = key
        self.left = None
        self.right = None

    def __repr__(self):
        return "{}".format(self.val)


class BST:
    def __init__(self, root):
        self.root = Node(root)

    def insert(self, root, key):
        if root is None:
            root = Node(key)
        else:
            if root.val < key:
                if root.right is None:
                    root.right = Node(key)
                else:
                    self.insert(root.right, key)
            else:
                if root.left is None:
                    root.left = Node(key)
                else:
                    self.insert(root.left, key)

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.val)
            self.inorder(root.right)

    def search(self, root, key):
        if root is None or key == root.val:
            return root

        if key > root.val:
            return self.search(root.right, key)

        return self.search(root.left, key)


bst = BST(50)
bst.insert(bst.root, 30)
bst.insert(bst.root, 20)
bst.insert(bst.root, 40)
bst.insert(bst.root, 70)
bst.insert(bst.root, 60)
bst.insert(bst.root, 80)

bst.inorder(bst.root)
print(bst.search(bst.root, 80))
bst = BST(10)
bst.insert(bst.root, 5)
bst.insert(bst.root, 15)
bst.insert(bst.root, 6)
bst.insert(bst.root, 20)

bst.inorder(bst.root)
