import random

arr1000 = [random.randint(0, 1000) for _ in range(1000)]
arr10000 = [random.randint(0, 10000) for _ in range(10000)]


def selection_sort(seq):
    for i in range(len(seq) - 1, 0 , -1):
        max_j = i
        for j in range(max_j):
            if seq[j] > seq[max_j]:
                max_j = j
            seq[i], seq[max_j] = seq[max_j], seq[i]
    return seq


print(selection_sort(arr1000))
print(selection_sort(arr10000))
