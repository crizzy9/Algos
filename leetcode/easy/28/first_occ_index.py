class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        s = -1
        n = len(needle)
        h = len(haystack)

        if n > h:
            return s
        for i in range(h-n+1):
            if needle == haystack[i:i+n]:
                s = i
                break

        return s

if __name__ == "__main__":
    s = Solution()
    assert s.strStr("sadbutsad", "sad") == 0
    assert s.strStr("leetcode", "leeto") == -1
    assert s.strStr("a", "a") == 0
    assert s.strStr("abc", "b") == 1
    assert s.strStr("abc", "c") == 2
