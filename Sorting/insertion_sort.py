import random

arr1000 = [random.randint(0, 1000) for _ in range(1000)]
arr10000 = [random.randint(0, 10000) for _ in range(10000)]


def insertion_sort(seq):
    for i in range(1, len(seq)):
        j = i
        while j > 0 and seq[j-1] > seq[j]:
            seq[j-1], seq[j] = seq[j], seq[j-1]
            j -= 1
    return seq


print(insertion_sort(arr1000[:]))
print(insertion_sort(arr10000[:]))

