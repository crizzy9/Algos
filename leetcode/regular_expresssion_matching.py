# https://leetcode.com/problems/regular-expression-matching/

class Solution:
    def isMatch(self, s, p):
        csi = 0
        i = 0
        print("Started s={} p={}".format(s, p))
        # write down all of the edge cases
        # convert pattern into matching how many numbers it will be easier
        while i < len(p):
            # csi = current string index
            print("i = {}, p[i] = {}, csi = {}".format(i, p[i], csi))
            if p[i].isalpha() and (i==len(p)-1 or (i < len(p)-1 and p[i+1] != '*')):
                # if s[csi-1]
                if len(s) == 0 or csi >= len(s):
                    csi += 1
                    break
                elif s[csi] != p[i]:
                    break
                else:
                    csi += 1
            elif p[i] == '.':
                csi += 1
            elif p[i] == '*':
                while csi < len(s):
                    # recursion to match it again
                    # edge case * is 1st
                    if i != 0 and p[i-1] != '*':
                        if p[i-1] != '.' and p[i-1] != s[csi]:
                            break
                        else:
                            csi += 1
            i += 1

        print('final csi = {}'.format(csi))

        if csi == len(s):
            return True
        else:
            return False


if __name__ == '__main__':
    sol = Solution()
    assert sol.isMatch("aa", "a") == False
    assert sol.isMatch("aa", "a*") == True
    assert sol.isMatch("ab", ".*") == True
    assert sol.isMatch("aab", "c*a*b") == True
    assert sol.isMatch("ccb", "c*a*b") == True
    assert sol.isMatch("ccaaab", "c*a*b") == True
    assert sol.isMatch("ccaaa", "c*a*b*") == True
    assert sol.isMatch("ccaaa", "c*a*b") == False
    assert sol.isMatch("ccaaa", "c*a*b*e*d") == False
    assert sol.isMatch("ccaaaaskdhakshdgfjhgasbadhsigh", "c*a*b*.*") == True
    assert sol.isMatch("mississippi", "mis*is*p*.") == False
    assert sol.isMatch("", ".ac") == False
    assert sol.isMatch("b", "b.bc") == False
    assert sol.isMatch("aaa", "a*a") == True
    assert sol.isMatch("aaa", "a*aa") == True
    assert sol.isMatch("aaabbbb", "a*aab*bb.*") == True
    assert sol.isMatch("aaabbbb", "a*aab*.b.") == True
