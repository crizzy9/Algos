class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        n = len(word1)
        m = len(word2)

        s = ""
        for i in range(max(n, m)):
            if i < n:
                s += word1[i]

            if i < m:
                s += word2[i]

        return s


if __name__ == "__main__":
    s = Solution()
    assert s.mergeAlternately("abc", "pqr") == "apbqcr"
    assert s.mergeAlternately("ab", "pqrs") == "apbqrs"
