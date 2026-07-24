class Logger:
    def __init__(self):
        self.msgs = {}

    def shouldPrintMessage(self, timestamp: int, message: str) -> bool:
        self.msgs.setdefault(message, 0)
        if timestamp >= self.msgs[message]:
            self.msgs[message] = timestamp + 10
            return True
        else:
            return False


# Your Logger object will be instantiated and called as such:
# obj = Logger()
# param_1 = obj.shouldPrintMessage(timestamp,message)

if __name__ == "__main__":
    s = Logger()

    assert s.shouldPrintMessage(1, "foo")
    assert s.shouldPrintMessage(2, "bar")
    assert not s.shouldPrintMessage(3, "foo")
    assert not s.shouldPrintMessage(8, "bar")
    assert not s.shouldPrintMessage(10, "foo")
    assert s.shouldPrintMessage(11, "foo")
