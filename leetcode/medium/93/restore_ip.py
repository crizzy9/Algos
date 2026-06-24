class Solution:
    def restoreIpAddresses(self, s: str) -> list[str]:

        if len(s) > 12:
            return []

        return []

    def isValid(self, s: str):
        parts = s.split(".")

        if len(parts) == 4 and all(
            [
                True if int(p) <= 255 and not (len(p) > 1 and p[0] == "0") else False
                for p in parts
            ]
        ):
            return True


if __name__ == "__main__":
    s = Solution()

    assert s.restoreIpAddresses("25525511135") == ["255.255.11.135", "255.255.111.35"]
    assert s.restoreIpAddresses("0000") == ["0.0.0.0"]
    assert s.restoreIpAddresses("101023") == [
        "1.0.10.23",
        "1.0.102.3",
        "10.1.0.23",
        "10.10.2.3",
        "101.0.2.3",
    ]
