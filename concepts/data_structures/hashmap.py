import re


class LinkedList:
    class Node:
        def __init__(self, value=None, pointer=None, count=1):
            self.value = value
            self.count = count
            # self.position = LinkedList()
            self.pointer = pointer

        def __repr__(self):
            return "Node(val={}, count={})".format(self.value, self.count)

    def __init__(self):
        self.head = None
        self.length = 0

    def __repr__(self):
        nodes = []
        node = self.head
        while node:
            nodes.append(node.__repr__())
            node = node.pointer
        return "LinkedList(" + ", ".join(nodes) + ")"

    def _add(self, value, count):
        self.length += 1
        self.head = self.Node(value, self.head, count)

    def insert(self, value, count):
        inc = self.increment(value, count)
        if not inc:
            self._add(value, count)

    # delete a node, given the previous node
    def delete(self, prev, node):
        self.length -= 1
        if not prev:
            self.head = node.pointer
        else:
            prev.pointer = node.pointer

    # locate node by value
    def _find_by_value(self, value):
        prev = None
        node = self.head
        while node:
            if node.value == value:
                break
            else:
                prev = node
                node = node.pointer
        return node, prev

    def increment(self, value, count=1):
        node, prev = self._find_by_value(value)
        if node:
            node.count += count
            return True
        else:
            return False

    def is_empty(self):
        if self.head:
            return False
        else:
            return True


class HashMap:
    def __init__(self):
        # number of keys collision will be handled using linked list
        self.k = 701
        self.keys = [LinkedList() for _ in range(self.k)]

    def insert(self, key, value):
        i = self.get_hash_index(key)
        self.keys[i].insert(key, value)

    def delete(self, key):
        i = self.get_hash_index(key)
        node, prev = self.keys[i]._find_by_value(key)
        if node:
            self.keys[i].delete(prev, node)
        else:
            print('Key with value {} not found'.format(key))

    def increase(self, key):
        i = self.get_hash_index(key)
        self.keys[i].increment(key)

    def find(self, key):
        i = self.get_hash_index(key)
        node, prev = self.keys[i]._find_by_value(key)
        return node

    def list_all_keys(self):
        return self.__repr__()

    def get_hash_index(self, string):
        n = len(string)
        m = 31
        hash_value = 0
        for s in string:
            hash_value += ord(s)*(m**(n-1))
        return hash_value % self.k

    def __repr__(self):
        # non_empty_list = [ll for ll in self.keys if not ll.is_empty()]
        # return "HashMap({})".format(non_empty_list)
        ret = 'HashMap(\n'
        for i, ll in enumerate(self.keys):
            ret += '\t'+str(i)+' : '+repr(ll) + '\n'
        return ret


if __name__ == '__main__':
    ll = LinkedList()
    ll.insert('this', 1)
    ll.insert('is', 1)
    ll.insert('shyams', 1)
    ll.insert("code", 2)
    print(ll)

    hm = HashMap()
    hm.insert("this", 1)
    hm.insert("is", 1)
    hm.insert("shyam", 1)
    hm.insert("this", 1)
    hm.insert("is", 1)
    hm.insert("lala", 1)
    hm.delete("is")
    print(hm)
    print(hm.find("shyam"))

    filename = 'alice_in_wonderland.txt'
    with open(filename, 'r', encoding='utf=8', errors='ignore') as f:
        data = re.sub(r'([\n\t ])+', ' ', f.read())
    words = data.split(' ')

    file_hm = HashMap()
    for word in words:
        file_hm.insert(word, 1)
    print(file_hm)
    file_hm.insert("random", 10)
    file_hm.increase("random")
    print(file_hm.find("random"))
    file_hm.delete("random")
    file_hm.increase("random")
    print(file_hm.find("random"))
    file_hm.increase("addition")
    print(file_hm.find("addition"))
