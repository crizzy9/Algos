class Solution:
    def wallsAndGates(self, rooms: list[list[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        EMPTY = 2147483647
        GATE = 0


if __name__ == "__main__":
    s = Solution()

    rooms = [
        [2147483647, -1, 0, 2147483647],
        [2147483647, 2147483647, 2147483647, -1],
        [2147483647, -1, 2147483647, -1],
        [0, -1, 2147483647, 2147483647],
    ]

    s.wallsAndGates(rooms)
    assert rooms == [[3, -1, 0, 1], [2, 2, 1, -1], [1, -1, 2, -1], [0, -1, 3, 4]]
