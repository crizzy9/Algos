class Solution:
    def isPalindrome(self, x: int) -> bool:
        num = str(x)
        return num[::-1] == num


if __name__ == "__main__":
    s = Solution()

    assert s.isPalindrome(121)
    assert s.isPalindrome(1234321)
    assert not s.isPalindrome(-121)
    assert not s.isPalindrome(10)
