class Solution:
    def insert(
        self, intervals: list[list[int]], newInterval: list[int]
    ) -> list[list[int]]:

        n = len(intervals)
        i = 0
        ans: list[list[int]] = []

        # interval not range of new then just add it
        while i < n and intervals[i][1] < newInterval[0]:
            ans.append(intervals[i])
            i += 1

        # interval in range of new one merge it
        while i < n and newInterval[1] >= intervals[i][0]:
            newInterval[0] = min(intervals[i][0], newInterval[0])
            newInterval[1] = max(intervals[i][1], newInterval[1])
            i += 1
        ans.append(newInterval)

        # interval not in range of new just add it
        while i < n:
            ans.append(intervals[i])
            i += 1

        return ans


if __name__ == "__main__":
    s = Solution()
    assert s.insert([[1, 3], [6, 9]], [2, 5]) == [[1, 5], [6, 9]]
    assert s.insert([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]) == [
        [1, 2],
        [3, 10],
        [12, 16],
    ]
