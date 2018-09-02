# https://leetcode.com/problems/longest-substring-without-repeating-characters/description/

class Solution:
    def lengthOfLongestSubstring(self, a):
        """
        :type a: str
        :rtype: int
        """
        s = a
        curr = ''
        longest = ''
        i = 0
        while i < len(a):
            try:
                ind = curr.index(a[i])
                a = a[ind+1:]
                i = 0
                if len(longest) < len(curr):
                    longest = curr
                curr = ''
            except ValueError as e:
                curr += a[i]
                if len(longest) < len(curr):
                    longest = curr
                i += 1

        return len(longest)

s = Solution()
s.lengthOfLongestSubstring("pwawkew")
s.lengthOfLongestSubstring("bcdpwawkew")
s.lengthOfLongestSubstring("pwawkalemkw")
s.lengthOfLongestSubstring("pwamkfpbwefjqbzaekw")

