import random

arr1000 = [random.randint(0, 1000) for _ in range(1000)]
arr10000 = [random.randint(0, 10000) for _ in range(10000)]


def quick_sort(seq):
    if len(seq) < 2:
        return seq

    ipivot = len(seq)//2
    pivot = seq[ipivot]
    before = [x for i,x in enumerate(seq) if x <= pivot and i != ipivot]
    after = [x for i,x in enumerate(seq) if x > pivot and i != ipivot]

    return quick_sort(before) + [pivot] + quick_sort(after)


print(quick_sort(arr1000))
print(quick_sort(arr10000))

