# https://leetcode.com/problems/string-to-integer-atoi/description/

class Solution:
    def myAtoi(self, string):
        """
        :type string: string
        :rtype: int
        """
        int_max = 2147483647
        int_min = -2147483648
        ans = ''
        string = string.strip()
        neg = False
        if string and string[0] == '-':
            string = string[1:]
            neg=True
        elif string and string[0] == '+':
            string = string[1:]

        if not string:
            return 0
        digits = [str(i) for i in range(10)]
        if string[0] not in digits:
            return 0

        for s in string:
            if s not in digits:
                break
            ans += s

        res = int(ans) if not neg else -int(ans)
        if res > int_max:
            return int_max
        elif res < int_min:
            return int_min
        else:
            return res


sol = Solution()
print(sol.myAtoi(""))
print(sol.myAtoi("        1398"))
print(sol.myAtoi("    -1398"))
print(sol.myAtoi("       -1398ghhas"))
print(sol.myAtoi("   asdhh1398"))
print(sol.myAtoi("  -asjh1398"))
print(sol.myAtoi("  -asjh1398hha"))

