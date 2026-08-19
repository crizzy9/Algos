from collections import Counter
import heapq


class Solution:
    def topKFrequent(self, words: list[str], k: int) -> list[str]:
        c = Counter(words)

        return heapq.nlargest(k, c.keys(), key=c.get)


if __name__ == "__main__":
    s = Solution()
    assert s.topKFrequent(["i", "love", "leetcode", "i", "love", "coding"], 2) == [
        "i",
        "love",
    ]
