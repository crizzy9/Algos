# https://leetcode.com/problems/word-pattern/description/
class Solution:
    def wordPattern(self, pattern, str):
        """
        :type pattern: str
        :type str: str
        :rtype: bool
        """

        words = str.split()
        if len(words) != len(pattern):
            return False

        i = 0
        mapping = {}
        reverse_map = {}
        res = True
        while i < len(words):
            if mapping.get(pattern[i]):
                if mapping[pattern[i]] == words[i]:
                    res = res and True
                else:
                    res = res and False
                    break
            elif reverse_map.get(words[i]):
                if reverse_map[words[i]] == pattern[i]:
                    res = res and True
                else:
                    res = res and False
                    break
            else:
                mapping[pattern[i]] = words[i]
                reverse_map[words[i]] = pattern[i]
            i += 1
        return res


sol = Solution()
print(sol.wordPattern('abba', "dog cat cat dog"))
print(sol.wordPattern('abba', "dog cat cat fish"))
print(sol.wordPattern('aaaa', "dog cat cat dog"))
print(sol.wordPattern('abba', "dog dog dog dog"))