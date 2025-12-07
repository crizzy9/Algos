def knapsack(weights, values, capacity, n):

    K = [[0 for _ in range(capacity+1)] for _ in range(n+1)]

    for i in range(n+1):
        for w in range(capacity+1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif weights[i-1] <= w:
                K[i][w] = max(values[i-1] + K[i-1][w-weights[i-1]], K[i-1][w])
            else:
                K[i][w] = K[i - 1][w]
    print(K)
    return K[n][W]

    # Without dp
    # if n == 0 or capacity == 0:
    #     return 0
    # if weights[n-1] > capacity:
    #     return knapsack(weights, values, capacity, n-1)
    # else:
    #     return max(values[n-1]+knapsack(weights, values, capacity-weights[n-1], n-1), knapsack(weights, values, capacity, n-1))


val = [60, 100, 120]
wt = [10, 20, 30]
W = 50
n = len(val)
print(knapsack(wt, val, W, n))