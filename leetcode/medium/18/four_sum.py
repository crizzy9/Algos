class Solution:
    def fourSum(self, nums: list[int], target: int) -> list[list[int]]:
        def kSum(nums: list[int], target: int, k: int) -> list[list[int]]:
            pass

        def twoSum(nums: list[int], target: int) -> list[list[int]]:
            s: set[int] = set()
            res: list[list[int]] = []

            for num in nums:
                comp = target - num
                if (len(res) == 0 or res[-1][1] != num) and comp in s:
                    res.append([comp, num])
                s.add(num)
            return res

        nums.sort()
        return kSum(nums, target, 4)


if __name__ == "__main__":
    sol = Solution()

    s1 = sol.fourSum([1, 0, -1, 0, -2, 2], 0)
    print(f"s1: {s1}")
    assert s1 == [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
