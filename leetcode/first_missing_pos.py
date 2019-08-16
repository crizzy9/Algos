class Solution:
    def firstMissingPositive(self, nums):
        all_nums = set(range(1, len(nums)+1))

        for n in nums:
            all_nums.discard(n)

        if len(all_nums) == 0:
            return len(nums)+1
        else:
            return min(all_nums)


if __name__ == '__main__':
    sol = Solution()
    assert sol.firstMissingPositive([1,2,0]) == 3
    assert sol.firstMissingPositive([3,4,-1,1]) == 2
    assert sol.firstMissingPositive([7,8,9,11,12]) == 1
