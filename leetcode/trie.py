class Node:
    def __init__(self, value, key=False):
        self.value = value
        self.key = key
        self.children = {}

    def __repr__(self):
        # return "Node({}, {}, {})".format(self.value, self.key, self.children)
        return self.rpr()

    def rpr(self, level=0):
        ret = "\t" * level + self.value + "\n"

        for child in self.children.values():
            ret += child.rpr(level + 1)
        return ret

class Trie:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root = Node('')

    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """
        node = self.root
        i = 0
        while i < len(word):
            if node.children.get(word[:i+1]):
                node = node.children[word[:i+1]]
                i += 1
            else:
                break

        while i < len(word):
            node.children[word[:i+1]] = Node(word[:i+1])
            node = node.children[word[:i+1]]
            i += 1
        if i == len(word):
            node.key = True

    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        node = self.root
        i = 0
        while i < len(word):
            if node.children.get(word[:i+1]):
                node = node.children[word[:i+1]]
                i += 1
            else:
                break
        if i == len(word) and node.key:
            return True
        else:
            return False

    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        node = self.root
        i = 0
        while i < len(prefix):
            if node.children.get(prefix[:i+1]):
                node = node.children[prefix[:i+1]]
                i += 1
            else:
                break

        if i == len(prefix):
            return True
        else:
            return False



    def __repr__(self):
        return "{}".format(self.root)

# Your Trie object will be instantiated and called as such:
obj = Trie()
obj.insert("a")
obj.insert("to")
obj.insert("tea")
obj.insert("ted")
obj.insert("ten")
obj.insert("i")
obj.insert("in")
obj.insert("inn")

print(obj)

print(obj.search("in"))
print(obj.search("tan"))
print(obj.search("ten"))

print(obj.startsWith("to"))
print(obj.startsWith("nv"))
print(obj.startsWith("in"))