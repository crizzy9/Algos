# https://leetcode.com/problems/gray-code/

class Solution:
    def grayCode(self, n):
        if n == 0:
            return [0]

        t = 2**n
        start ='0'*n
        seq = set()
        res = [start]
        seq.add(start)

        for i in range(t):
            last = res[-1]
            for j in range(n-1, -1, -1):
                new = list(last)
                new[j] = str(1 - int(new[j]))
                new = ''.join(new)
                if new not in seq:
                    res.append(new)
                    seq.add(new)
                    break

        return [int(r, 2) for r in res]

    def grayCode2(self, n):
        return [i ^ (i >> 1) for i in range(1 << n)]



if __name__ == '__main__':
    sol = Solution()
    print("For 2")
    print(sol.grayCode(2))
    print("For 3")
    print(sol.grayCode(3))
    print("For 4")
    print(sol.grayCode(4))


    print("For 2")
    print(sol.grayCode2(2))
    print("For 3")
    print(sol.grayCode2(3))
    print("For 4")
    print(sol.grayCode2(4))

