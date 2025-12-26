class Solution:
    def getPassword(self, inp):
        s = 50
        p = 0

        for i in inp:
            if i[0] == "L":
                s = s - int(i[1:])
                while s < 0:
                    s = 100 + s
            if i[0] == "R":
                s = s + int(i[1:])
                while s > 99:
                    s = abs(100 - s)

            # print(f"current s: {s}")
            if s == 0:
                p += 1

        return p

    def getPassword2(self, inp):
        s = 50
        p = 0

        for i in inp:
            if i[0] == "L":
                news = s - int(i[1:])
                while news < 0:
                    news = 100 + news
                    if s > 0 and news < 100:
                        p += 1
                s = news

            if i[0] == "R":
                news = s + int(i[1:])
                while news > 99:
                    news = abs(100 - news)
                    if s < 99  and news > 0:
                        p += 1
                s = news

            # print(f"current s={s} p={p}")
            if s == 0:
                p += 1

        return p


if __name__ == "__main__":
    sol = Solution()

    # s = sol.getPassword(["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"])
    # print("password:", s)
    #
    # with open("/home/nightwatcher/personal/dev/Algos/aoc/2025/day1/input.txt", "r") as f:
    #     inp = f.readlines()
    #
    # s = sol.getPassword(inp)
    # print("password:", s)

    s = sol.getPassword2(["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"])
    print("password:", s)

    with open("/home/nightwatcher/personal/dev/Algos/aoc/2025/day1/input.txt", "r") as f:
        inp = f.readlines()

    s = sol.getPassword2(inp)
    print("password:", s)
