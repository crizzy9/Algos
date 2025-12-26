class Solution:
    def longestPalindrome(self, s):
        n = len(s)
        dp = [[False]*n for _ in range(n)]
        ans = [0,0]

        for i in range(n):
            dp[i][i] = True

        for i in range(n-1):
            if s[i] == s[i+1]:
                dp[i][i+1] = True
                ans = [i,i+1]

        for d in range(2, n):
            for i in range(n-d):
                j = i + d
                if s[i] == s[j] and dp[i+1][j-1]:
                    dp[i][j] = True
                    ans = [i, j]

        return s[ans[0]:ans[1]+1]


if __name__ == "__main__":
    s = Solution()

    ans = s.longestPalindrome("babad")
    print(ans)
    assert (ans == "aba" or ans == "bab")

    ans = s.longestPalindrome("cbbd")
    print(ans)
    assert (ans == "bb")

    ans = s.longestPalindrome("racecar")
    print(ans)
    assert (ans == "racecar")
