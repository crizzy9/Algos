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

    def isMatchRecursive(self, text, pattern):
        if not pattern:
            return not text

        first = bool(text) and pattern[0] in {text[0], '.'}

        if len(pattern) >= 2 and pattern[1] == '*':
            return self.isMatchRecursive(text, pattern[2:]) or self.isMatchRecursive(text[1:], pattern)
        else:
            return self.isMatchRecursive(text[1:], pattern[1:])


if __name__ == '__main__':
    sol = Solution()

    examples = [("aa", "a", False), ("aa", "a*", True), ("ab", ".*", True), ("aab", "c*a*b", True), ("ccb", "c*a*b", True), ("ccaaab", "c*a*b", True), ("ccaaa", "c*a*b*", True), ("ccaaa", "c*a*b", False), ("ccaaa", "c*a*b*e*d", False), ("ccaaaaskdhakshdgfjhgasbadhsigh", "c*a*b*.*", True), ("mississippi", "mis*is*p*.", False), ("", ".ac", False), ("b", "b.bc", False), ("aaa", "a*a", True), ("aaa", "a*aa", True), ("aaabbbb", "a*aab*bb.*", True), ("aaabbbb", "a*aab*.b.", True)]

    for ex in examples:
        s, p, r = ex
        print(s, p, r)
        # assert sol.isMatch(s, p) == r
        assert sol.isMatchRecursive(s, p) == r

    print("All Tests passed!")

