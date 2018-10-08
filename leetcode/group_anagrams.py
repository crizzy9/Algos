# https://leetcode.com/problems/group-anagrams/description/

class Solution:
    def groupAnagrams(self, strs):
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """
        group_dict = {}

        for s in strs:
            str_set = set(s)
            group_dict.setdefault(str_set, []).append(s)

        print(group_dict)


sol = Solution()
sol.groupAnagrams(['eat', 'tan', 'ate', 'tea', 'nat', 'bat'])
