
# https://leetcode.com/problems/roman-to-integer/description/
class Solution:
    def romanToInt(self, s: str) -> int:
        smap = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000,
        }

        # write a function convert string s from roman to integer in O(n) time using the smap
        # iterate through the string
        # if the current character is less than the next character, subtract the current character from the next character
        # else add the current character to the sum
        # return the sum

        sum = 0
        for i in range(len(s)):
            if i < len(s) - 1 and smap[s[i]] < smap[s[i + 1]]:
                sum -= smap[s[i]]
            else:
                sum += smap[s[i]]

        return sum

if __name__ == '__main__':
    s = Solution()
    assert s.romanToInt('III') == 3
    assert s.romanToInt('LVIII') == 58
    assert s.romanToInt('MCMXCIV') == 1994
