class Solution:
    def rob(self, nums: list[int]) -> int:
        s1 = 0
        s2 = 0

        for i in range(len(nums)):
            if i == 0 or i % 2 == 0:
                s1 += nums[i]
            else:
                s2 += nums[i]

        return max(s1, s2)


if __name__ == "__main__":
    s = Solution()
    assert s.rob([1, 2, 3, 1]) == 4
    assert s.rob([2, 7, 9, 3, 1]) == 12
    assert s.rob([2, 1, 1, 2]) == 4
