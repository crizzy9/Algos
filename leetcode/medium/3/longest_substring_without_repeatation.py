# https://leetcode.com/problems/longest-substring-without-repeating-characters/description/

class Solution:
    # Beats 72.19 % of python3 solutions
    def lengthOfLongestSubstring(self, a):
        cd = {} 
        i = 0
        j = 0
        longest = ''
        while j < len(a):
            cf = cd.get(a[j], -1)
            if cf >= i:
                i = cf + 1
            cd[a[j]] = j
            j += 1
            if len(a[i:j]) > len(longest):
                longest = a[i:j]
        return len(longest)

s = Solution()
print(s.lengthOfLongestSubstring("pwawkew"))
print(s.lengthOfLongestSubstring("bcdpwawkew"))
print(s.lengthOfLongestSubstring("pwawkalemkw"))
print(s.lengthOfLongestSubstring("pwamkfpbwefjqbzaekw"))
print(s.lengthOfLongestSubstring("ajhfgdshp18y2304cnuqwkkankbrhlbjpqo02-o;aslg.mdlnfoyt0294uivm=i[plkasm.,dnjksdbfgzkbcx,jngksmdfj,[pyktjorjh9ty7829479810-9=orkspfdljnbfjkbzbxnkc.mzxn,mv ncbvagfuygdyukqpoweklgndnkdh irotmhugfib[pvnsbcrg,dimhxgvjtyegshuxjkr[kbhtpg8y2u-nfmpcbyt809p4nq67oiwvybnua smjtghdknfskzljnbry1ui26q7w5ufijd[m2p;3owe7utnim[0q'wpa;oly5bnucop,2mus8nupv5w8no7o"))
