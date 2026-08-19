class Solution:
    def subarraySum(self, nums: list[int], k: int) -> int:
        c, s = 0, 0
        map = {0: 1}

        for i in range(len(nums)):
            s += nums[i]
            if (s - k) in map:
                c += map[s - k]
            map[s] = map.get(s, 0) + 1

        return c


if __name__ == "__main__":
    s = Solution()
    assert s.subarraySum([1, 1, 1], 2) == 2
    assert s.subarraySum([1, 2, 3], 3) == 2
    assert s.subarraySum([1, 1, 5], 2) == 1
    assert s.subarraySum([1, 1, 5], 3) == 0
