# https://leetcode.com/problems/generate-parentheses/description/
class Solution:
    # Beats 60.22% python3 submissions
    def generateParenthesis(self, n):
        out = []
        combs = [('(', 1)]
        while combs:
            curr, openings  = combs.pop()
            if len(curr) + openings == 2*n:
                curr += ')'*openings
                out.append(curr)
            else:
                if openings == 0:
                    combs.append((curr + '(', openings + 1))
                else:
                    combs.append((curr + '(', openings + 1))
                    combs.append((curr + ')', openings - 1))
        print(len(out))
        return out


s = Solution()
print(s.generateParenthesis(3))
print(s.generateParenthesis(4))
print(s.generateParenthesis(5))
print(s.generateParenthesis(6))
print(s.generateParenthesis(7))
