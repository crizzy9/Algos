def bfs_iterative(graph, start):
    queue, visited = [start], [False]*len(graph)

    while queue:
        vertex = queue.pop(0)
        for neighbor in graph[vertex]:
            if not visited[neighbor]:
                queue.append(neighbor)
                visited[neighbor] = True



