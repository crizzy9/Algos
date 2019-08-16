# https://leetcode.com/problems/search-in-rotated-sorted-array/

class Solution:
    def search(self, nums, target):
        return self.recursive_search(nums, target, 0, len(nums)-1)

    def recursive_search(self, nums, target, l, r):
        if l > r:
            return -1

        mid = (l + r)//2
        print("l={}, r={}, mid={}".format(l, r, mid))
        print("nums={}, target={}, nums[mid]={}".format(nums, target, nums[mid]))

        if target == nums[mid]:
            return mid

        if nums[mid] >= nums[l]:
            if target >= nums[l] and target <= nums[mid]:
                return self.recursive_search(nums, target, l, mid-1)
            return self.recursive_search(nums, target, mid+1, r)

        if target >= nums[mid] and target <= nums[r]:
            return self.recursive_search(nums, target, mid+1, r)
        return self.recursive_search(nums, target, l, mid-1)


if __name__ == '__main__':
    sol = Solution()
    assert sol.search([4,5,6,7,0,1,2], 0) == 4
    assert sol.search([4,5,6,7,0,1,2], 3) == -1
    assert sol.search([4,5,6,7,8,10,12,0,1,2], 3) == -1
    assert sol.search([4,5,6,7,8,10,12,0,1,2], 12) == 6
