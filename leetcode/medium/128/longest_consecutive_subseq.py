class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        if len(nums) == 0:
            return 0
        numset = set(nums)

        longest_streak = 1

        for num in numset:
            if num - 1 not in numset:
                curr = num
                curr_streak = 1
                while curr + 1 in numset:
                    curr += 1
                    curr_streak += 1

                longest_streak = max(curr_streak, longest_streak)
        return longest_streak

    def longestConsecutiveOld(self, nums: list[int]) -> int:
        nums.sort()

        longest_streak = 1
        current_streak = 1

        for i in range(1, len(nums)):
            if nums[i] != nums[i - 1]:
                if nums[i] == nums[i - 1] + 1:
                    current_streak += 1
                else:
                    longest_streak = max(current_streak, longest_streak)
                    current_streak = 1

        return max(longest_streak, current_streak)


if __name__ == "__main__":
    s = Solution()

    assert s.longestConsecutive([100, 4, 200, 1, 3, 2]) == 4
    assert s.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert s.longestConsecutive([0, 3, 3, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert s.longestConsecutive([1, 0, 1, 2]) == 3
