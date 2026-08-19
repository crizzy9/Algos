class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        n = len(nums)
        out = []
        for i in range(n):
            if nums[i] > 0:
                break

            # handle duplicates
            if i == 0 or nums[i - 1] != nums[i]:
                seen = set()
                j = i + 1
                while j < n:
                    complement = -nums[i] - nums[j]
                    if complement in seen:
                        out.append([nums[i], nums[j], complement])
                        # handle duplicates
                        while j + 1 < n and nums[j] == nums[j + 1]:
                            j += 1
                    seen.add(nums[j])
                    j += 1

        return out


if __name__ == "__main__":
    s = Solution()
    print(s.threeSum([-1, 0, 1, 2, -1, -4]))
    print(s.threeSum([0, 1, 1]))
    print(s.threeSum([0, 0, 0]))
