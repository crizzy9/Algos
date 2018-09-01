# https://leetcode.com/problems/longest-substring-without-repeating-characters/description/

class Solution:
    def lengthOfLongestSubstring(self, s):
        final_max = ''
        new_max = ''
        for c in s:
            if c in new_max:
                ind = new_max.index(c)
                if len(new_max) >= len(final_max):
                    final_max = new_max
                print(ind)
                new_max = new_max[ind+1:]
                print(new_max)
            else:
                new_max += c
        print(final_max)

s = Solution()
s.lengthOfLongestSubstring("pwawkew")
s.lengthOfLongestSubstring("bcdpwawkew")

