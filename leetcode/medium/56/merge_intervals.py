class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        inp = sorted(intervals,key=lambda x: x[0])
        out: list[list[int]] = []
        curr = inp[0]
        for i in range(1, len(inp)):
            if inp[i][0] <= curr[1]:
                curr[1] = max(curr[1], inp[i][1])
            else:
                out.append(curr)
                curr = inp[i]
        out.append(curr)
        return out

if __name__ == "__main__":
    s = Solution()
    assert s.merge([[1,3],[5,7],[2,6],[8,10],[15,18],[24,27],[21,25]]) == [[1,7],[8,10],[15,18],[21,27]]
    assert s.merge([[1,4],[2,3]]) == [[1,4]]
