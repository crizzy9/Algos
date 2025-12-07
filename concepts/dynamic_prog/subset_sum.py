# geeks for geeks problem


def subset_sum(lst, target, n):

    if target == 0:
        return True
    if n == 0 and target != 0:
        return False

    if lst[n-1] > target:
        return subset_sum(lst, target, n-1)

    return subset_sum(lst, target, n-1) or subset_sum(lst, target-lst[n-1], n-1)


print(subset_sum([3, 34, 4, 12, 5, 2], 9, 6))

