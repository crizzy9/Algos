import math
import collections


class Solution:
    def maximumDetonation(self, bombs: list[list[int]]) -> int:
        graph = collections.defaultdict(list)
        n = len(bombs)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                x1, y1, r1 = bombs[i]
                x2, y2, _ = bombs[j]

                d = math.dist((x1, y1), (x2, y2))

                if r1 >= d:
                    graph[i].append(j)

        def dfs(i):
            stack = [i]
            visited = set([i])
            while stack:
                c = stack.pop()
                for neighbor in graph[c]:
                    if neighbor not in visited:
                        stack.append(neighbor)
                        visited.add(neighbor)

            return len(visited)

        ans = 0
        for i in range(n):
            ans = max(ans, dfs(i))

        return ans


if __name__ == "__main__":
    s = Solution()
    assert s.maximumDetonation([[2, 1, 3], [6, 1, 4]]) == 2
    assert s.maximumDetonation([[1, 1, 5], [10, 10, 5]]) == 1
    assert (
        s.maximumDetonation([[1, 2, 3], [2, 3, 1], [3, 4, 2], [4, 5, 3], [5, 6, 4]])
        == 5
    )
