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


class TabManager:
    def __init__(self, homepage: str):
        self.homepage: str = homepage
        self.current_tab: int = 0
        self.tabs: dict[int, BrowserHistory] = {0: BrowserHistory(self.homepage)}

    def open_tab(self):
        self.current_tab += 1
        self.tabs[self.current_tab] = BrowserHistory(self.homepage)

    def switch_tab(self, tab_id: int):
        pass

    def close_tab(self, tab_id: int):
        pass

    def visit(self, url: str):
        pass

    def back(self, steps: int) -> str:
        pass

    def forward(self, steps: int) -> str:
        pass

    def get_current_url(self) -> str:
        pass


if __name__ == "__main__":
    print("Running updated CodeSignal test cases...")

    # Initialize Manager with the default homepage
    tm = TabManager("chime.com")

    # Test Case 1: Open first tab (Implicit ID 1)
    tm.open_tab()
    assert tm.get_current_url() == "chime.com", "Failed to set initial active tab"

    # Test Case 2: Visit URLs in active tab
    tm.visit("chime.com/about")
    tm.visit("chime.com/careers")
    assert tm.get_current_url() == "chime.com/careers", (
        "Failed to visit URL in active tab"
    )

    # Test Case 3: Open second tab (Implicit ID 2, should steal focus)
    tm.open_tab()
    assert tm.get_current_url() == "chime.com", (
        "New tab did not start at default homepage"
    )

    # Test Case 4: Isolate histories
    tm.switch_tab(1)
    assert tm.get_current_url() == "chime.com/careers", "Tab 1 history was overwritten"
    assert tm.back(1) == "chime.com/about", "Back tracking failed on Tab 1"

    # Test Case 5: Complex navigation on secondary tab
    tm.switch_tab(2)
    tm.visit("github.com")
    tm.visit("leetcode.com")
    assert tm.back(1) == "github.com", "Back tracking failed on Tab 2"
    assert tm.forward(1) == "leetcode.com", "Forward tracking failed on Tab 2"

    # Test Case 6: Open third tab (Implicit ID 3), close it, and check fallback logic
    tm.open_tab()
    assert tm.get_current_url() == "chime.com"
    tm.close_tab(3)
    # The active tab should fall back to the most recently opened tab that is still open (tab 2)
    assert tm.get_current_url() == "leetcode.com", (
        f"Expected leetcode.com (tab 2), got {tm.get_current_url()}"
    )

    # Test Case 7: Close remaining tabs
    tm.close_tab(2)
    assert tm.get_current_url() == "chime.com/about", "Fallback to tab 1 failed"
    tm.close_tab(1)
    assert tm.get_current_url() is None, "Should return None when all tabs are closed"

    print("All test cases passed!")
