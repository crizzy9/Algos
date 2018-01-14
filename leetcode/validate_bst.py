# https://leetcode.com/problems/validate-binary-search-tree/description/
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

    def __repr__(self):
        return "TreeNode({})".format(self.val)

class Solution:

    def __init__(self):
        self.res = []

    def isValidBST(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """
        self.res = []
        self.inorder(root)
        # print("Inorder seq:", self.res)
        ans = True
        for i in range(len(self.res) - 1):
            if self.res[i] >= self.res[i+1]:
                ans = False
                break
        return ans

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            self.res.append(root.val)
            self.inorder(root.right)



sol = Solution()
r = TreeNode(1)
r.left = TreeNode(2)
r.right = TreeNode(3)
r2 = TreeNode(2)
r2.left = TreeNode(1)
r2.right = TreeNode(3)
print(sol.isValidBST(r))
print(sol.isValidBST(r2))
r3 = TreeNode(1)
r3.right = TreeNode(1)
print(sol.isValidBST(r3))
r4 = TreeNode(10)
r4.left = TreeNode(5)
r4.right = TreeNode(15)
r4.right.left = TreeNode(6)
r4.right.right = TreeNode(20)
print(sol.isValidBST(r4))
