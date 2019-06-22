# https://leetcode.com/problems/positions-of-large-groups
class Solution:
    def largeGroupPositions(self, S):
        start = 0
        end = 0
        res = []
        print("input string:", S)

        for i in range(len(S)):
            print("i", i)
            print("c", S[i], "prev_c", S[i-1])
            print("start", start)
            print("end", end)
            if S[i] == S[i-1] and i != 0:
                end += 1
            if i == len(S)-1 or S[i] != S[i-1]:
                if end - start >= 2:
                    res.append([start, end])
                start = i
                end = i

        print("out:", res)
        return res

if __name__ == '__main__':
    sol = Solution()
    out = sol.largeGroupPositions("abcdddeeeeaabbbcd")
    assert out == [[3,5],[6,9],[12,14]]

    out = sol.largeGroupPositions("aaa")
    assert out ==[[0,2]]

    # out = sol.largeGroupPositions("kajhhhhsjdjhajkhhhjksahdkjhhhkjhqwheiouhnbbxqiueyuiyqvbvvvviutqwbetqwvb tqwuytuyetqytyyyyyyweyttqgebhbg")
