class BrowserHistory:
    def __init__(self, homepage: str):
        self.curr: int = 0
        self.history: list[str] = [homepage]

    def visit(self, url: str) -> None:
        self.curr += 1
        # if at the middle somewhere delete the forward history
        self.history = self.history[: self.curr]
        self.history.append(url)

    def back(self, steps: int) -> str:
        self.curr -= steps
        if self.curr < 0:
            self.curr = 0
        return self.history[self.curr]

    def forward(self, steps: int) -> str:
        self.curr += steps
        if self.curr > len(self.history) - 1:
            self.curr = len(self.history) - 1
        return self.history[self.curr]


if __name__ == "__main__":
    browserHistory = BrowserHistory("leetcode.com")

    browserHistory.visit("google.com")
    browserHistory.visit("facebook.com")
    browserHistory.visit("youtube.com")
    assert browserHistory.back(1) == "facebook.com"
    assert browserHistory.back(1) == "google.com"
    assert browserHistory.forward(1) == "facebook.com"
    browserHistory.visit("linkedin.com")
    assert browserHistory.forward(2) == "linkedin.com"
    assert browserHistory.back(2) == "google.com"
    assert browserHistory.back(7) == "leetcode.com"
