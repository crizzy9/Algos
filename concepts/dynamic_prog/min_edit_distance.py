from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

def min_edit_distance(source, target):
    n = len(source)
    m = len(target)

    dist = [[0 for _ in range(n+1)] for _ in range(m+1)]
    pp.pprint(dist)
    for i in range(1, n+1):
        dist[i][0] = dist[i-1][0] + 1
    pp.pprint(dist)
    for j in range(1, m+1):
        dist[0][j] = dist[0][j-1] + 1
    pp.pprint(dist)

    for i in range(1, n+1):
        for j in range(1, m+1):
            dist[i][j] = min(dist[i-1][j] + 1, dist[i-1][j-1] + (0 if source[i-1] == target[j-1] else 2), dist[i][j-1] + 1)
    # pp.pprint(dist)
    return dist[n][m]


if __name__ == '__main__':
    print(min_edit_distance("intention", "execution"))
