class Solution:
    def isValid(self, s: str) -> bool:
        stack: list[str] = []

        for b in s:
            if b == "(":
                stack.append(b)
            if b == ")":
                if len(stack) > 0 and stack[-1] == "(":
                    stack.pop()
                else:
                    return False
            if b == "{":
                stack.append(b)
            if b == "}":
                if len(stack) > 0 and stack[-1] == "{":
                    stack.pop()
                else:
                    return False
            if b == "[":
                stack.append(b)
            if b == "]":
                if len(stack) > 0 and stack[-1] == "[":
                    stack.pop()
                else:
                    return False

        if len(stack) == 0:
            return True
        return False


if __name__ == "__main__":
    s = Solution()
    assert s.isValid("()")
    assert s.isValid("()[]{}")
    assert not s.isValid("([]{}")
    assert not s.isValid("(]{}")
    assert s.isValid("({[]})")
    assert not s.isValid("[(")
    assert not s.isValid(")]")
