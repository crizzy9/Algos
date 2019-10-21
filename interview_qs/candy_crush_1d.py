# Bloomberg interview qs
# ccaabbbacd -> d
class Solution:
    def candy_crush(self, line):

        stack = []
        i = 0
        while i < len(line):
            print("i={}, stack={}, line[i]={}".format(i, stack, line[i]))
            if len(stack)!=0:
                if line[i] == stack[-1]:
                    stack.append(line[i])
                    i+=1
                else:
                    if len(stack) >= 3 and stack[-1] == stack[-2] and stack[-1] == stack[-3]:
                        x = stack.pop()
                        while len(stack)!=0 and stack[-1]==x:
                            print('x={}, stack={}'.format(x, stack))
                            stack.pop()
                    else:
                        stack.append(line[i])
                        i+=1
            else:
                stack.append(line[i])
                i += 1

        if len(stack) >= 3 and stack[-1] == stack[-3]:
            x = stack.pop()
            while len(stack)!=0 and stack[-1]==x:
                print('x={}, stack={}'.format(x, stack))
                stack.pop()

        print("Final Stack: {}".format("".join(stack)))
        return ''.join(stack)


if __name__ == '__main__':
    sol = Solution()
    assert sol.candy_crush('ccaabbbacd') == 'd'
    assert sol.candy_crush('aabbbacd') == 'cd'
    assert sol.candy_crush('ddccaabbbacdefffigghhhgi') == 'eii'
    assert sol.candy_crush('ccaabbbac') == ''
    assert sol.candy_crush('dccaabbbacdffiighhhggiffd') == ''
    print(sol.candy_crush('ccaabebacd'))

    print("All done")

