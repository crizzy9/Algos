from collections import deque
q = deque(["buffy", "xander", "willow"])
print(q)
q.append("dalit")
print(q)
print(q.popleft())
print(q.pop())
q.appendleft("shamu")
print(q)
