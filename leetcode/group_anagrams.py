# https://leetcode.com/problems/group-anagrams/description/

class Solution:
    def groupAnagrams(self, strs):
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """
        groups = []
        group_sets = []

        for s in strs:
            str_set = set(s)
            if str_set not in group_sets:
                group_sets.append(str_set)
                groups.append([s])
            else:
                groups[group_sets.index(str_set)].append(s)

        print(groups)


sol = Solution()
sol.groupAnagrams(['eat', 'tan', 'ate', 'tea', 'nat', 'bat'])
