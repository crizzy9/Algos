class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def __repr__(self):
        return "TreeNode({})".format(self.val)


# recursive solution is trivial, what about iteratively
def inorder_recursive(res, root):
    if root:
        inorder_recursive(res, root.left)
        res.append(root.al)
        inorder_recursive(res, root.right)


def inorder_iter(root):
    # basically dfs only
    if root is None:
        return []
    stack = [(root, 1)]
    res = []
    while stack:
        r, v = stack.pop()
        if v == 0:
            res.append(r.val)

        if r.right is not None and v == 1:
            stack.append((r.right, 1))
        # put this at the end for preorder traversal
        # put this at top for postorder traversal
        if v == 1:
            stack.append((r, 0))
        if r.left is not None and v == 1:
            stack.append((r.left, 1))
    return res


r4 = TreeNode(10)
r4.left = TreeNode(5)
r4.right = TreeNode(15)
r4.right.left = TreeNode(6)
r4.right.right = TreeNode(20)

print(inorder_iter(r4))

r = TreeNode(50)
r.left = TreeNode(30)
r.right = TreeNode(70)
r.left.left = TreeNode(20)
r.left.right = TreeNode(40)
r.right.left = TreeNode(60)
r.right.right = TreeNode(80)

print(inorder_iter(r))

