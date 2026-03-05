class Solution:
    def jump(self, nums: list[int]) -> int:
        n = len(nums)
        s = 0
        i = 0
        if n == 1:
            return 0
        while i < n:
            c = nums[i]
            if i + c == n - 1:
                s += 1
                break
            elif i == n -1:
                break
            elif i + c < n:
                max_index, _ = max(enumerate(nums[i:c+1]), key=lambda x: x[1])
                i = max_index
                s += 1
            else:
                i += 1
                s += 1

        return s

    def jump2(self, nums: list[int]) -> int:
        s, n = 0, len(nums)
        curr_end, curr_far = 0, 0

        for i in range(n-1):
            curr_far = max(curr_far, i+nums[i])

            if i == curr_end:
                s += 1
                curr_end = curr_far

        return s

if __name__ == "__main__":
    s = Solution()

    assert s.jump2([2,3,1,1,4]) == 2
    assert s.jump2([2,3,0,1,4]) == 2
    assert s.jump2([0]) == 0
    assert s.jump2([1,2]) == 1
    assert s.jump2([2,1]) == 1
    assert s.jump2([3,2,1]) == 1
