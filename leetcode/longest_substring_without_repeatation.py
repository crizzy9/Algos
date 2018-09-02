# https://leetcode.com/problems/longest-substring-without-repeating-characters/description/
from collections import Counter

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
        
        print('algo1: longest unique substring for {} is {} with length: {}'.format(s, longest, len(longest)))
        return len(longest)

    # Beats 48.59% of submissions 112ms
    def lengthOfLongestSubstring2(self, a):
        # create char freq dict
        cd = Counter(a)
        cd = {k:[v, -1] for k, v in cd.items()}
        i = 0
        j = 0
        longest = ''
        while j < len(a):
            cf = cd.get(a[j])
            if cf[1] >= i:
                i = cf[1]+1
            cf[1] = j
            cf[0] -= 1
            j += 1
            if len(a[i:j]) > len(longest):
                longest = a[i:j]
        print('algo2: longest unique substring for {} is {} with length: {}'.format(a, longest, len(longest)))
        return len(longest)

s = Solution()
s.lengthOfLongestSubstring("pwawkew")
s.lengthOfLongestSubstring("bcdpwawkew")
s.lengthOfLongestSubstring("pwawkalemkw")
s.lengthOfLongestSubstring("pwamkfpbwefjqbzaekw")

s.lengthOfLongestSubstring2("pwawkew")
s.lengthOfLongestSubstring2("bcdpwawkew")
s.lengthOfLongestSubstring2("pwawkalemkw")
s.lengthOfLongestSubstring2("pwamkfpbwefjqbzaekw")

#s.lengthOfLongestSubstring2("ajhfgdshp18y2304cnuqwankbrhlbjpqo02-o;aslg.mdlnfoyt0294uivm=i[plkasm.,dnjksdbfgzkbcx,jngksmdfj,[pyktjorjh9ty7829479810-9=orkspfdljnbfjkbzbxnkc.mzxn,mv ncbvagfuygdyukqpoweklgndnkdh irotmhugfib[pvnsbcrg,dimhxgvjtyegshuxjkr[kbhtpg8y2u-nfmpcbyt809p4nq67oiwvybnua smjtghdknfskzljnbry1ui26q7w5ufijd[m2p;3owe7utnim[0q'wpa;oly5bnucop,2mus8nupv5w8no7o")
