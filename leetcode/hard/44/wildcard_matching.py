class Solution:
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        print("start: ", s, p)
        pattern = {}
        i = 0
        prev = 0
        for c in p:
            if c == '*' or c == '?':
                if prev:
                    i += 1
                    prev = 0
                pattern[i] = c
                if not prev:
                    i += 1
            elif pattern.get(i):
                pattern[i] += c
            else:
                pattern[i] = c
                prev = 1

        i = 0
        j = 0
        while i < len(pattern.keys()):
            if pattern[i] == '*':
                if pattern.get(i+1):
                    x = ''
                    while j < len(s):
                        x += s[j]
                        j += 1
                        if x[-len(pattern[i+1]):] == pattern[i+1]:
                            break
                    i += 1
                else:
                    return True
            elif pattern[i] == '?':
                i += 1
            else:
                x = ''
                while j < len(s):
                    x += s[j]
                    j += 1
                    if x == pattern[i]:
                        break
                i += 1


        print("i: {} j: {}".format(i, j))
        print("pattern:", pattern)
        if i == len(pattern):
            return True
        else:
            return False


sol = Solution()
print(sol.isMatch("aa", "a"))
print(sol.isMatch("aa", "aa"))
print(sol.isMatch("aaa", "aa"))
print(sol.isMatch("aa", "*"))
print(sol.isMatch("aa", "a*"))
print(sol.isMatch("ab", "?*"))
print(sol.isMatch("aab", "c*a*b*"))
print(sol.isMatch("cab", "c*a*b*"))
print(sol.isMatch("cccaaaa", "c*a*b*"))
print(sol.isMatch("cccaaaab", "c*a*"))
print(sol.isMatch("cccaaaabb", "c*a*b*"))
print(sol.isMatch("abefcdgiescdfimde", "ab*cd?i*de"))
print(sol.isMatch("aaaa", "***a"))


