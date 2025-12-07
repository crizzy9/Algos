import random

arr1000 = [random.randint(0, 1000) for _ in range(1000)]
arr10000 = [random.randint(0, 10000) for _ in range(10000)]


def gnome_sort(seq):
    i = 0
    while i < len(seq):
        if i == 0 or seq[i-1] <= seq[i]:
            i +=1
        else:
            seq[i], seq[i-1] = seq[i-1], seq[i]
            i-=1
        return seq


print(gnome_sort(arr1000))
print(gnome_sort(arr10000))

