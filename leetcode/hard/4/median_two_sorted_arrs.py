class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """

        sorted_arr = []
        head1 = 0
        head2 = 0
        while head1 < len(nums1) and head2 < len(nums2):
            if nums1[head1] < nums2[head2]:
                sorted_arr.append(nums1[head1])
                head1 += 1
            else:
                sorted_arr.append(nums2[head2])
                head2 += 1
        if head1 < len(nums1):
            sorted_arr.extend(nums1[head1:])
        elif head2 < len(nums2):
            sorted_arr.extend(nums2[head2:])

        tot_len = (len(nums1) + len(nums2))
        if tot_len % 2 == 0:
            x = tot_len // 2
            return (sorted_arr[x-1] + sorted_arr[x])/2
        else:
            return sorted_arr[tot_len//2]



sol = Solution()
print(sol.findMedianSortedArrays([1,2,3,5], [4,6,8,9]))
print(sol.findMedianSortedArrays([1,2], [3,4]))
