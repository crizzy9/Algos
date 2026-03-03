class Solution:
    def countAndSay(self, n: int) -> str:
        if n == 1:
            return "1"

        return self.rle(self.countAndSay(n-1))

    def rle(self, num: str) -> str:
        counter = 1
        s = ""
        i = 0
        while i < len(num) - 1:
            if num[i + 1] == num[i]:
                i += 1
                counter += 1
            else:
                s += str(counter) + str(num[i])
                counter = 1
                i += 1

        s += str(counter) + str(num[-1])
        return s

if __name__ == "__main__":
    s = Solution()

    assert s.countAndSay(4) == "1211"
    assert s.countAndSay(5) == "111221"
