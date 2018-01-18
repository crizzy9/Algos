# Kth smallest element in a row-wise and column-wise sorted 2D array | Set 1
#
# Given an n x n matrix, where every row and column is sorted in non-decreasing order. Find the kth smallest element in the given 2D array.
#
# For example, consider the following 2D array.
#
# 10, 20, 30, 40
# 15, 25, 35, 45
# 24, 29, 37, 48
# 32, 33, 39, 50
# The 3rd smallest element is 20 and 7th smallest element is 30


# check diagonal elements

def kth_smallest(arr, k):
    sorted_arr = []

    i = 0
    while i < len(arr):
        sorted_arr.extend(sorted([arr[i-k][k] for k in range(i+1)]))
        i += 1
    print(sorted_arr)


a = [
    [10, 20, 30, 40],
    [15, 25, 35, 45],
    [24, 29, 37, 48],
    [32, 33, 39, 50]
]

kth_smallest(a,3)