# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def __repr__(self):
        return "{}->({}, {})".format(self.val, self.left, self.right)

class Solution:

    def buildTree(self, preorder, inorder):
        """
        :type preorder: List[int]
        :type inorder: List[int]
        :rtype: TreeNode
        """
        head = None
        # preorder as a queue
        if preorder:
            elem = preorder.pop(0)
            for i in range(len(inorder)):
                if elem == inorder[i]:
                    head = TreeNode(elem)
                    head.left = self.buildTree(preorder[:i], inorder[:i])
                    head.right = self.buildTree(preorder[i:], inorder[i+1:])
                    break
        return head

# tree = TreeNode(1)
# tree.left = TreeNode(2)
# tree.left.left = TreeNode(4)
# tree.left.right = TreeNode(5)
# tree.left.right.left = TreeNode(8)
# tree.left.right.right = TreeNode(9)
# tree.right = TreeNode(3)
# tree.right.left = TreeNode(6)
# tree.right.right = TreeNode(7)

inorder_seq = [4, 2, 8, 5, 9, 1, 6, 3, 7]
preorder_seq = [1, 2, 4, 5, 8, 9, 3, 6, 7]

sol = Solution()
print(sol.buildTree(preorder_seq, inorder_seq))

# sol = Solution()
print(sol.buildTree([-1], [-1]))
