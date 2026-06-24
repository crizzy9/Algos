from functools import lru_cache


class Solution:
    def numDecodings(self, s: str) -> int:
        return self.rec(s, 0)

    @lru_cache(maxsize=None)
    def rec(self, s: str, index: int):
        if index == len(s):
            return 1

        if s[index] == "0":
            return 0

        if index == len(s) - 1:
            return 1

        ans = self.rec(s, index + 1)
        if int(s[index : index + 2]) <= 26:
            ans += self.rec(s, index + 2)

        return ans


if __name__ == "__main__":
    s = Solution()

    assert s.numDecodings("12") == 2
    assert s.numDecodings("226") == 3
    assert s.numDecodings("06") == 0
