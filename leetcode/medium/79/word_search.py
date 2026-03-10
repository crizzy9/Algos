class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        return True

if __name__ == "__main__":
    s = Solution()
    assert s.exist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED") == True
    assert s.exist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "SEE") == True
    assert s.exist([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB") == False
