class Solution:
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """

        if len(s) < numRows:
            return s
        ref = {}
        i = 1
        inc = True
        for c in s:
            ref.setdefault(i, []).append(c)
            if i < numRows and inc:
                i += 1
            elif i == 1 and not inc:
                i += 1
                inc =True
            elif i > 1:
                i -= 1
                inc = False
        print(ref)
        zigzag_str = ''
        for j in range(1, numRows+1):
            zigzag_str += ''.join(ref[j])
        return zigzag_str





sol = Solution()
assert sol.convert("PAYPALISHIRING", 3) == 'PAHNAPLSIIGYIR'
assert sol.convert("PAYPALISHIRING", 4) == 'PINALSIGYAHRPI'
assert sol.convert("PAYPALISHIRING", 5) == 'PHASIYIRPLIGAN'
print("All tests passed")

