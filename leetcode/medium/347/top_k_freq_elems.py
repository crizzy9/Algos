from collections import Counter


class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        # max heap based soln on counter

        counter = Counter(nums)
        return [i[0] for i in counter.most_common(k)]


if __name__ == "__main__":
    s = Solution()
    assert s.topKFrequent([1, 1, 1, 2, 2, 3], 2) == [1, 2]
    assert s.topKFrequent([1, 2, 1, 2, 1, 2, 3, 1, 3, 2], 2) == [1, 2]
    assert s.topKFrequent([1], 1) == [1]
