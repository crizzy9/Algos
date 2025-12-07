import sys


class BinomialHeap:
    class Node:
        def __init__(self, key=None, child=None, parent=None, sibling=None, degree=0):
            self.key = key
            self.child = child
            self.parent = parent
            self.sibling = sibling
            self.degree = degree

        def __repr__(self):
            return "{" + "key: {}, degree: {}, child: {}, sibling: {}".format(self.key, self.degree, self.child, self.sibling) + "}"

    def __init__(self):
        self.head = None
        self.min_key = sys.maxsize

    def insert(self, key):
        if self.head is None:
            self.head = self.Node(key=key)
        else:
            self.head = self.union(self.head, self.Node(key=key))

    def _merge(self, h1, h2):
        new_heap = self.Node()
        curr = new_heap
        n1 = h1
        n2 = h2
        while n1 is not None and n2 is not None:
            if n1.degree == n2.degree:
                h1 = h1.sibling
                h2 = h2.sibling
                curr.sibling = n1
                n2.sibling = None
                curr.sibling.sibling = n2
                curr = curr.sibling.sibling
                n1 = h1
                n2 = h2
            elif n1.degree < n2.degree:
                h1 = h1.sibling
                curr.sibling = n1
                n1.sibling = None
                curr = curr.sibling
                n1 = h1
            else:
                h2 = h2.sibling
                curr.sibling = n2
                n2.sibling = None
                curr = curr.sibling
                n2 = h2

        if n1 is None and n2 is not None:
            curr.sibling = n2
        elif n1 is not None and n2 is None:
            curr.sibling = n1
        new_heap = new_heap.sibling
        return new_heap

    # where y.key <= x.key
    def _link(self, x, y):
        x.sibling = y.child
        y.child = x
        x.parent = y
        y.degree += 1

    def union(self, h1, h2):
        dummy_head = self._merge(h1, h2)
        prev_x = None
        x = dummy_head
        next_x = x.sibling
        while next_x is not None:
            if (x.degree != next_x.degree) or (next_x.sibling is not None and next_x.sibling.degree == x.degree):
                prev_x = x
                x = next_x
                next_x = next_x.sibling
            elif x.key <= next_x.key:
                x.sibling = next_x.sibling
                self._link(next_x, x)
                next_x = x.sibling
            else:
                if prev_x is None:
                    dummy_head = next_x
                else:
                    prev_x.sibling = next_x
                self._link(x, next_x)
                x = next_x
                next_x = x.sibling
        return dummy_head

    # return min, prev_node min
    def min(self):
        node = self.head
        prev = None
        min_prev = None
        el = None
        while node is not None:
            if self.min_key > node.key:
                self.min_key = node.key
                min_prev = prev
                el = node
            prev = node
            node = node.sibling
        return el, min_prev

    def extract_min(self):
        node, node_prev = self.min()
        # data leak
        node_prev.sibling = node.sibling
        prev = node.child
        curr = prev.sibling
        nxt = curr.sibling

        while curr is not None:
            if prev.parent.child == prev:
                prev.sibling = None
            prev.parent = None
            curr.sibling = prev

            prev = curr
            curr = nxt
            if nxt is not None:
                nxt = nxt.sibling

        old_heap = self.head
        new_heap = prev
        self.head = self.union(old_heap, new_heap)

    def delete(self, key):
        self.decrease_key(key, -sys.maxsize)
        self.extract_min()

    # x -> initial value, k -> value to replace with
    def decrease_key(self, x, k):
        if x < k:
            raise ValueError("Value to replace with should be less than the value already there")
        node = self._find(x)
        if node is None:
            raise ValueError("Value {} not found in Heap".format(x))
        node.key = k
        p = node.parent
        while p is not None and node.key < p.key:
            node.key, p.key = p.key, node.key
            node = p
            p = node.parent

    def _find(self, key):
        stack = [self.head]
        el = None
        while stack:
            node = stack.pop()
            if node.key == key:
                el = node
                break
            if node.sibling is not None:
                stack.append(node.sibling)
            if node.child is not None:
                stack.append(node.child)
        return el

    def _display(self, root):
        ret = ''
        stack = [(root, 0)]
        while stack:
            node, height = stack.pop()
            if node is None:
                continue
            if node.sibling is not None:
                stack.append((node.sibling, height))
            if node.child is not None:
                stack.append((node.child, height + 1))

            if node.parent is not None and node.parent.child != node:
                offset = '|\t' * height
            elif node.parent is None:
                offset = ''
            else:
                offset = '-\t'
            ret += offset + str(node.key)
            if len(stack) == 0 or stack[-1][1] <= height:
                ret += '\n'
        print("Binomial Heap with head @", root.key)
        return ret

    def __repr__(self):
        return self._display(self.head)


if __name__ == '__main__':
    bh = BinomialHeap()
    keys = [20,11,7,57,90,65,92,95,84,82,51,94,42,25,18,85,47,39,34,40,20,38,22,97,41]
    for i in keys:
        bh.insert(i)
    print(bh)
    print("Find 90: ", bh._find(90))
    print("Min:", bh.min())
    bh.decrease_key(25, 6)
    print("Decreased key: 25 to 6")
    print(bh)
    print("Extracting minimum:")
    bh.extract_min()
    print(bh)
    print("After delete 34:")
    bh.delete(34)
    print(bh)
