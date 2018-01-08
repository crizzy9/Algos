class Node:
    def __init__(self, value):
        self.value = value
        self.children = {}

    def __repr__(self):
        return "Node({}, {})".format(self.value, self.children)

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

    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """





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

# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)