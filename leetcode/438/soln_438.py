from typing import Counter

class Solution:
    def findAnagrams(self, s: str, p: str) -> list[int]:
        cp = Counter(p)
        ans = []
        if len(p) > len(s):
            return []
        else:
            for i in range(len(s)):
                sb = s[i : i + len(p)]
                uc = Counter(sb)
                if uc == cp:
                    ans.append(i)
        return ans
