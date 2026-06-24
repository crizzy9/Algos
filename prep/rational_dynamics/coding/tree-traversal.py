# https://www.hackerrank.com/challenges/tree-preorder-traversal/problem?isFullScreen=true
class Node:
    def __init__(self, info):
        self.info = info
        self.left = None
        self.right = None
        self.level = None

    def __str__(self):
        return str(self.info)


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def create(self, val):
        if self.root == None:
            self.root = Node(val)
        else:
            current = self.root

            while True:
                if val < current.info:
                    if current.left:
                        current = current.left
                    else:
                        current.left = Node(val)
                        break
                elif val > current.info:
                    if current.right:
                        current = current.right
                    else:
                        current.right = Node(val)
                        break
                else:
                    break

    def __str__(self):
        if self.root is None:
            return "(empty tree)"

        def _subtree_grid(node):
            """Returns (char_grid, node_col) — grid is list[list[str]], node_col is centre column."""
            label = str(node.info)
            width = len(label)

            if node.left is None and node.right is None:
                return [list(label)], width // 2

            left_grid = [] if node.left is None else _subtree_grid(node.left)[0]
            right_grid = [] if node.right is None else _subtree_grid(node.right)[0]

            lh = len(left_grid)
            rh = len(right_grid)
            max_h = max(lh, rh)

            def pad_grid(grid, h):
                if not grid:
                    return [[" "] * (len(grid[0]) if grid else 0) for _ in range(h)]
                w = len(grid[0])
                while len(grid) < h:
                    grid.append([" "] * w)
                return grid

            left_grid = pad_grid(left_grid, max_h)
            right_grid = pad_grid(right_grid, max_h)

            lw = len(left_grid[0]) if left_grid else 0
            rw = len(right_grid[0]) if right_grid else 0

            has_left = node.left is not None
            has_right = node.right is not None

            if has_left and has_right:
                gap = max(2, width + 2)
            else:
                gap = 1

            total_w = lw + gap + rw
            node_col = lw + gap // 2

            out = []

            row0 = [" "] * max(total_w, node_col + (width + 1) // 2)
            start = node_col - width // 2
            for i, ch in enumerate(label):
                row0[start + i] = ch
            out.append(row0)

            row1 = [" "] * len(row0)
            if has_left:
                row1[node_col - 1] = "/"
            if has_right:
                row1[node_col + 1] = "\\"
            out.append(row1)

            for r in range(max_h):
                out.append(left_grid[r] + [" "] * gap + right_grid[r])

            return out, node_col

        grid, _ = _subtree_grid(self.root)
        return "\n".join("".join(row).rstrip() for row in grid)


"""
Node is defined as
self.left (the left child of the node)
self.right (the right child of the node)
self.info (the value of the node)
"""


def preOrder(root):
    # Write your code here
    stack, path = [root], []
    while stack:
        v = stack.pop()
        if v in path:
            continue
        path.append(v)
        if v.right is not None:
            stack.append(v.right)
        if v.left is not None:
            stack.append(v.left)
    print(" ".join(map(lambda x: str(x.info), path)))


def postOrder(root):
    # Write your code here
    stack, path = [root], []

    while stack:
        v = stack[-1]

        if (v.left in path or v.left is None) and (v.right in path or v.right is None):
            path.append(v)
            stack.pop()

        if v.right is not None and v not in path:
            stack.append(v.right)

        if v.left is not None and v not in path:
            stack.append(v.left)

    print(" ".join(map(lambda x: str(x.info), path)))


def inOrder(root):
    res = []

    def inorder_rec(res, root):
        if root:
            inorder_rec(res, root.left)
            res.append(root)
            inorder_rec(res, root.right)

    inorder_rec(res, root)

    print(" ".join(map(lambda x: str(x.info), res)))


def levelOrder(root):
    que, visited = [root], []

    while que:
        v = que.pop(0)

        visited.append(v)

        if v.left is not None and v.left not in visited:
            que.append(v.left)

        if v.right is not None and v.right not in visited:
            que.append(v.right)

    print(" ".join(map(lambda x: str(x.info), visited)))


tree = BinarySearchTree()

# t = int(input())
# arr = list(map(int, input().split()))

t = 6
arr = [1, 2, 5, 3, 6, 4]

for i in range(t):
    tree.create(arr[i])

print()
print(tree)
print()
# preOrder(tree.root)
# postOrder(tree.root)
# inOrder(tree.root)
levelOrder(tree.root)
