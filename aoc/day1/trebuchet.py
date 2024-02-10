import time

class Trebuchet:
    # with one loop
    def getCalibrationValues(self, inputs) -> int:
        calibs = []
        for inp in inputs:
            s = 0
            e = len(inp) - 1
            sbreak = ebreak = False
            while True:
                if not sbreak and not inp[s].isdigit():
                    s += 1
                else:
                    sbreak = True

                if not ebreak and not inp[e].isdigit():
                    e -= 1
                else:
                    ebreak = True

                if sbreak and ebreak:
                    break
            calibs.append(int(inp[s]+inp[e]))

        return sum(calibs)

    # with 2 loops
    def getCalibrationValues2(self, inputs) -> int:
        calibs = []
        for inp in inputs:
            # print(f'Processing input: {inp}')
            s = 0
            e = len(inp) - 1
            while True:
                if not inp[s].isdigit():
                    s += 1
                else:
                    break
            while True:
                if not inp[e].isdigit():
                    e -= 1
                else:
                    break

            calibs.append(int(inp[s]+inp[e]))

        return sum(calibs)
    
    # add 2 numbers and get their average
    def part2(self, a, b):
        pass


if __name__ == "__main__":
    # https://adventofcode.com/2023/day/1
    t = Trebuchet()

    # test 1
    inps = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]

    out = t.getCalibrationValues(inps)
    if out == 142:
        print("Success!!!")
    else:
        print("FAIL :( ... actual value: ", out)

    out2 = t.getCalibrationValues2(inps)
    if out2 == 142:
        print("Success!!!")
    else:
        print("FAIL :( ... actual value: ", out2)

    # measure performance? memory and time

    # Part 1
    with open('aoc/treb_input.txt', 'r') as f:
        finput = f.readlines()

    ## method 1
    start = time.time()
    outx = t.getCalibrationValues(finput)
    end = time.time()
    print(f'Method 1 - Output: {outx} ... took {end - start} seconds')

    ## method 2
    start2 = time.time()
    outx2 = t.getCalibrationValues2(finput)
    end2 = time.time()
    print(f'Method 2 - Output: {outx2} ... took {end2 - start2} seconds')



