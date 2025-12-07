import random

arr1000 = [random.randint(0, 1000) for _ in range(1000)]
arr10000 = [random.randint(0, 10000) for _ in range(10000)]


def merge_sort(seq):
    if len(seq) < 2:
        return seq
    mid = len(seq)//2
    left = merge_sort(seq[:mid])
    right = merge_sort(seq[mid:])

    res = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1

    if left[i:]:
        res.extend(left[i:])
    if right[j:]:
        res.extend(right[j:])
    return res


print(merge_sort(arr1000))
print(merge_sort(arr10000))
