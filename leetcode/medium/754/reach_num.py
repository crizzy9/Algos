class Solution:
    def reachNumber(self, target):
        """
        :type target: int
        :rtype: int
        """

        # tuple structure (curr, step)
        # starts at 0 at step 0
        queue = [(0, 0)]
        while queue:
            curr, step = queue.pop(0)
            if curr == target:
                return step
            else:
                move = step + 1
                queue.append((curr+move, move))
                queue.append((curr-move, move))
        return None

sol = Solution()
print(sol.reachNumber(1000000))