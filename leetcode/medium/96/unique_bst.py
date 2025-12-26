# https://leetcode.com/problems/unique-binary-search-trees/
class Solution:
    def numTrees(self, n):
        # the number of unique trees is actually the catalan numbers
        # t(n) = total num of unique trees with n nodes
        # let i be any node from 1 -> n
        # then in a tree with i as the root there are
        # (i-1) nodes less than i; hence will be in the left subtree
        # (n-i) nodes greater than i; hence will be in the right subtree
        # total number of trees with i as the root is t(i-1)*t(n-i) since left and right trees are independent
        # Therefore total number of trees with n nodes is
        # t(n) = sum_(i=1->n) t(i-1)*t(n-i)
        # t(0) = t(1) = 1
        # https://www.geeksforgeeks.org/total-number-of-possible-binary-search-trees-with-n-keys/

        # numbers are 0->n and then eventually -1 for 0th
        t = [1]*2 + [0]*(n-1)
        for i in range(2, n+1):
            for j in range(1, i+1):
                t[i] += t[j-1] * t[i-j]
        return t[-1]




if __name__ == '__main__':
    sol = Solution()
    assert sol.numTrees(3) == 5
    assert sol.numTrees(4) == 14
    assert sol.numTrees(5) == 42
    assert sol.numTrees(6) == 132
    assert sol.numTrees(7) == 429
