class Solution:
    def validWordAbbreviation(self, word: str, abbr: str) -> bool:
        c = []
        for l in abbr:
            cx = ""
            if l.isdigit():
                cx += l
            else:
                cx = ""

        return True


if __name__ == "__main__":
    s = Solution()
    assert s.validWordAbbreviation("substitution", "s10n")
    assert not s.validWordAbbreviation("substitution", "s55n")
