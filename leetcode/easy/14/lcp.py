class Solution:
    def longestCommonPrefix(self, strs: list[str]) -> str:
        if len(strs) == 0:
            return ""
        p = strs[0]
        for i in range(1, len(strs)):
            while strs[i].find(p) != 0:
                p = p[: len(p) - 1]
                if p == "":
                    return ""
        return p


if __name__ == "__main__":
    s = Solution()

    assert s.longestCommonPrefix(["flower", "flow", "flight"]) == "fl"
    assert s.longestCommonPrefix(["dog", "racecar", "car"]) == ""
