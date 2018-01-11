class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        compliments = {}
        out = []
        for i in range(len(nums)):
            compliment = target-nums[i]
            if compliment in compliments:
                out = [i+1, compliments.get(compliment)+1]
                break
            else:
                compliments[nums[i]] = i
        return out

sol = Solution()
print(sol.twoSum([2,3,4], 6))