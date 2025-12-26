# Find a sorted subsequence of size 3 in linear time
# 3.3
# Given an array of n integers, find the 3 elements such that a[i] < a[j] < a[k] and i < j < k in 0(n) time. If there are multiple such triplets, then print any one of them.
#
# Examples:
#
# Input: arr[] = {12, 11, 10, 5, 6, 2, 30}
# Output: 5, 6, 30
#
# Input: arr[] = {1, 2, 3, 4}
# Output: 1, 2, 3 OR 1, 2, 4 OR 2, 3, 4
#
# Input: arr[] = {4, 3, 2, 1}
# Output: No such triplet

import sys


def sorted_subseq(arr):
    min1 = sys.maxsize
    min2 = sys.maxsize
    min3 = 0

    for a in arr:

        if min1 > a:
            min1 = a
        elif min2 > a:
            min2 = a
        else:
            min3 = a
            break

    return [min1, min2, min3]


def sorted_subseq_n(arr, n):
    seq = [sys.maxsize]*n
    for a in arr:
        for i in range(len(seq)):
            if seq[i] > a:
                seq[i] = a
                break
    return seq


a1 = [12, 11, 10, 5, 6, 2, 30]
a2 = [6, 9, 5, 7, 8, 4, 10]
print(sorted_subseq(a1))
print(sorted_subseq(a2))
print(sorted_subseq_n(a1, 3))
print(sorted_subseq_n(a2, 3))



