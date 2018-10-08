# https://leetcode.com/problems/group-anagrams/description/
from collections import Counter

#really bad solution -> better algo
class Solution:
    def groupAnagrams(self, strs):
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """
        groups = []
        group_sets = []

        for s in strs:
            str_set = Counter(s)
            try:
                groups[group_sets.index(str_set)].append(s)
            except Exception as e:    
                group_sets.append(str_set)
                groups.append([s])

        print(groups)


sol = Solution()
sol.groupAnagrams(['eat', 'tan', 'ate', 'tea', 'nat', 'bat'])
sol.groupAnagrams(["hos","boo","nay","deb","wow","bop","bob","brr","hey","rye","eve","elf","pup","bum","iva","lyx","yap","ugh","hem","rod","aha","nam","gap","yea","doc","pen","job","dis","max","oho","jed","lye","ram","pup","qua","ugh","mir","nap","deb","hog","let","gym","bye","lon","aft","eel","sol","jab"])
