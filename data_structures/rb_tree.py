from enum import Enum


class Color(Enum):
    BLACK = 'BLACK'
    RED = 'RED'


class RBNode:
    def __init__(self, value, color=Color.RED, parent=None, left=None, right=None):
        self.value = value
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

    def is_sentinel(self):
        if self.value is None:
            return True
        else:
            return False

    def is_root(self):
        if self.parent.value is None and self.value is not None:
            return True
        else:
            return False

    def tree_rep(self, level=0):
        v = (self.value, 'R' if self.color == Color.RED else 'B')
        ret = "\t\t"*level+'|' + str(v) + "\n"
        for child in [self.left, self.right]:
            if child is None or child.value is None:
                continue
            ret += child.tree_rep(level+1)
        return ret

    def __repr__(self):
        return self.tree_rep()
        # if self.value is not None:
        #     return "({}, {}) : [{}, {}]".format(self.value, self.color, self.left, self.right)
        # else:
        #     return "N"


class RedBlackTree:
    def __init__(self, arr):
        # sentinel
        self.sentinel = RBNode(None)
        self.root = self.sentinel
        for a in arr:
            # create node with just value
            v = RBNode(a)
            self.insert(v)

    def __repr__(self):
        return "{}".format(self.root)

    # def tree_rep(self):
    #     level = self.get_tree_height()
    #     # ret = "\t"*level+repr(self.value)+"\n"
    #     ret = ''
    #     queue = [(self.root, level)]
    #     path = []
    #     while queue:
    #         v, l = queue.pop(0)
    #         if level != l:
    #             ret += '\n'
    #             level -= 1
    #         ret += '\t'*l+str(v.value)
    #
    #         if v in path:
    #             continue
    #         path.append((v, l))
    #
    #         if not v.left.is_sentinel():
    #             queue.append((v.left,l-1))
    #         if not v.right.is_sentinel():
    #             queue.append((v.right,l-1))
    #     print([(p[0].value, p[1]) for p in path])
    #     print(ret)

    def get_tree_height(self):
        n = self.root
        h = 0
        while not n.is_sentinel():
            h += 1
            n = n.left
        return h

    def insert(self, z):
        # print("Inserting", z)
        y = self.sentinel
        x = self.root
        while x != self.sentinel:
            y = x
            if z.value < x.value:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == self.sentinel:
            self.root = z
        elif z.value < y.value:
            y.left = z
        else:
            y.right = z

        z.left = self.sentinel
        z.right = self.sentinel
        z.color = Color.RED
        print("Before fixup")
        print(self.__repr__())
        self.insert_fixup2(z)
        print("After fixup")
        print(self.__repr__())

    def insert_fixup2(self, z):
        z.color = Color.RED
        while z != self.root and z.parent.color == Color.RED:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y and y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y and y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.left_rotate(z.parent.parent)
        self.root.color = Color.BLACK

    def insert_fixup(self, z):
        while z.parent.color == Color.RED:
            if z.parent.parent is None and self.get_tree_height() <= 1:
                break
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                elif z == z.parent.right:
                    z = z.parent
                    self.left_rotate(z)
                else:
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.BLACK
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                elif z == z.parent.left:
                    z = z.parent
                    self.right_rotate(z)
                else:
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.BLACK
                    self.left_rotate(z.parent.parent)
        self.root.color = Color.BLACK

    def _transplant(self, u , v):
        if u.parent.is_sentinel():
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, v):
        z = self.search(v)
        y = z
        y_org_color = y.color
        if z.left.is_sentinel():
            x = z.right
            self._transplant(z, z.right)
        elif z.right.is_sentinel():
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._min(z.right)
            y_org_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_org_color == Color.BLACK:
            self.delete_fixup(x)

    def delete_fixup(self, x):
        while not x.is_root() and x.color == Color.BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                elif w.right.color == Color.BLACK:
                    w.left.color = Color.BLACK
                    w.color = Color.RED
                    self.right_rotate(w)
                    w = x.parent.right
                w.color = x.parent.color
                x.parent.color = Color.BLACK
                w.right.color = Color.BLACK
                self.left_rotate(x.parent)
                x = self.root
            else:
                if x == x.parent.right:
                    w = x.parent.left
                    if w.color == Color.RED:
                        w.color = Color.BLACK
                        x.parent.color = Color.RED
                        self.right_rotate(x.parent)
                        w = x.parent.left
                    if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
                        w.color = Color.RED
                        x = x.parent
                    elif w.left.color == Color.BLACK:
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = Color.BLACK

    def search(self, val):
        head = self.root
        while not head.is_sentinel():
            if head.value == val:
                break
            elif val < head.value:
                head = head.left
            else:
                head = head.right
        if head.is_sentinel():
            print("No such element found")
        else:
            return head

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.sentinel:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.sentinel:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.sentinel:
            x.right.parent = y
        x.parent = y.parent
        if y.parent == self.sentinel:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    @staticmethod
    def _min(node):
        while not node.left.is_sentinel():
            node = node.left
        return node.value

    def min(self):
        return self._min(self.root)

    @ staticmethod
    def _max(node):
        while not node.right.is_sentinel():
            node = node.right
        return node.value

    def max(self):
        return self._max(self.root)

    def sort(self):
        return self._inorder_traversal(self.root)

    def _inorder_traversal(self, root):
        if root is None:
            return []
        stack = [(root, 1)]
        res = []
        while stack:
            r, v = stack.pop()
            if v == 0 and not r.is_sentinel():
                res.append(r.value)

            if r.right is not None and v == 1:
                stack.append((r.right, 1))
            if v == 1:
                stack.append((r, 0))
            if r.left is not None and v == 1:
                stack.append((r.left, 1))
        return res

    def successor(self, val):
        node = self.search(val)
        if not node.right.is_sentinel():
            return node.right
        else:
            while True:
                if not node.is_root():
                    if node == node.parent.left:
                        return node.parent
                    else:
                        node = node.parent
                else:
                    break
            return "{} does not have any successors.".format(val)

    def predecessor(self, val):
        node = self.search(val)
        if not node.left.is_sentinel():
            return node.left
        else:
            while True:
                if not node.is_root():
                    if node == node.parent.right:
                        return node.parent
                    else:
                        node = node.parent
                else:
                    break
            return "{} does not have any predecessor.".format(val)


rbt = RedBlackTree([3,6,8,1,2])
rbt.insert(RBNode(4))
print(rbt)
print(rbt.get_tree_height())
# print(rbt.tree_rep())
# print("min=", rbt.min())
# print("max=", rbt.max())
# print(rbt.sort())
# print(rbt.search(3))
# print(rbt.successor(8))
# print(rbt.predecessor(8))
#
# print("rbt before delete: 3")
# print(rbt)
# rbt.delete(3)
# print(rbt)
