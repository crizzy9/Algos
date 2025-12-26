# https://leetcode.com/problems/maximum-sum-of-3-non-overlapping-subarrays
class Solution:
    def maxSumOfThreeSubarrays(self, nums, K):
        # Criteria
        # All 3*K elements sum must be maximum
        # Only 3 subarrays of size K
        # choose final answer that is lexicographically smallest when competing answers exists (smaller indices)

        # * get all inital seeds (subarrays of size 3) and call itself so you get a recurrsion like max(seed1 + maxSum(rest of array), seed2 + ..... seed_n)
        # Create an array of sums of subarrays by using a sliding window the indices that it has are the starting indices of the subarrays
        # Goal: array = seeds, window size = K, find a tuple (i,j,k) of indices from seeds that maximizes the sum seeds[i] + seeds[j] + seeds[k]
        # They should be non overlapping so i + K <= j and j + K <= k
        # And they should be lexicographically smallest
        print(nums, K)

        W = []
        for i in range(len(nums)-K+1):
            W.append(sum(nums[i:i+K]))
        print(W)

        left = [0] * len(W)
        best = 0
        for i in range(len(W)):
            if W[i] > W[best]:
                best = i
            left[i] = best
        print(left)

        right = [0] * len(W)
        best = len(W) - 1
        for i in range(len(W) - 1, -1, -1):
            if W[i] >= W[best]:
                best = i
            right[i] = best
        print(right)

        return None

if __name__ == '__main__':
    sol = Solution()
    assert sol.maxSumOfThreeSubarrays([1,2,1,2,6,7,5,1], 2) == [0,3,5]
