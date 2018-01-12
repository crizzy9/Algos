class Solution:
    def letterCombinations(self, digits):
        """
        :type digits: str
        :rtype: List[str]
        """
        mapping = {2: 'abc', 3: 'def', 4: 'ghi', 5: 'jkl', 6: 'mno', 7: 'pqrs', 8: 'tuv', 9: 'wxyz'}
        out = []
        for digit in digits:
            if not out:
                out = [i for i in mapping[int(digit)]]
            else:
                curlen = len(out)
                for i in range(curlen):
                    for l in mapping[int(digit)]:
                        out.append(out[i]+l)
                out = out[curlen:]
        return out


sol = Solution()
print(sol.letterCombinations('23'))
print(sol.letterCombinations('23452'))

