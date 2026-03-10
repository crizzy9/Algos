class Solution:
    def intToRoman(self, num: int) -> str:
        digits = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I")
        ]

        r: list[str] = []
        for v, s in digits:
            if num == 0:
                break
            c, num = divmod(num, v)
            r.append(s*c)

        return "".join(r)

if __name__ == "__main__":
    s = Solution()

    assert s.intToRoman(58) == "LVIII"
    assert s.intToRoman(1994) == "MCMXCIV"
    assert s.intToRoman(3749) == "MMMDCCXLIX"
    assert s.intToRoman(3999) == "MMMCMXCIX"
