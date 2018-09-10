# https://leetcode.com/problems/generate-parentheses/description/
class Solution:
    # Beats 43.77% python3 submissions
    def generateParenthesis(self, n):
        out = []
        combs = [('(', ['('])]
        while combs:
            curr, curr_stack = combs.pop()
            if len(curr) + len(curr_stack) == 2*n:
                while curr_stack:
                    curr_stack.pop()
                    curr += ')'
                out.append(curr)
            else:
                new_stack = curr_stack.copy()
                new_stack.append('(')

                if len(curr_stack) == 0:
                    combs.append((curr + '(', new_stack))
                else:
                    combs.append((curr + '(', new_stack))
                    curr_stack.pop()
                    combs.append((curr + ')', curr_stack))
        print(len(out))        
        return out


s = Solution()
print(s.generateParenthesis(3))
print(s.generateParenthesis(4))
print(s.generateParenthesis(5))
print(s.generateParenthesis(6))
print(s.generateParenthesis(7))
