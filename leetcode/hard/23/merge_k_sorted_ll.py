# Definition for singly-linked list.
from operator import itemgetter
import sys

class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

    def __repr__(self):
        return "{}->{}".format(self.val, self.next)

class Solution:
    def mergeKLists(self, lists):
        """
        :type lists: List[ListNode]
        :rtype: ListNode
        """
        sortedNode = None
        head = None
        while any(True for l in lists if l is not None):
            # could put it in a min heap and pop elements (better solution?)
            # or you can use priority queue
            to_choose = []
            for i in range(len(lists)):
                if lists[i] is not None:
                    to_choose.append(lists[i].val)
                else:
                    to_choose.append(sys.maxsize)
            # print("sorted: {}, lists: {}, to_choose: {}".format(sortedNode, lists, to_choose))
            min_index, min_val = min(enumerate(to_choose), key=itemgetter(1))
            if sortedNode is None:
                head = ListNode(min_val)
                sortedNode = head
            else:
                head.next = ListNode(min_val)
                head = head.next
            lists[min_index] = lists[min_index].next

        return sortedNode



list1 = ListNode(7)
list1.next = ListNode(9)
list1.next.next = ListNode(11)
list1.next.next.next = ListNode(12)
list1.next.next.next.next = ListNode(15)
list1.next.next.next.next.next = ListNode(19)

list2 = ListNode(1)
list2.next = ListNode(8)
list2.next.next = ListNode(10)
list2.next.next.next = ListNode(14)
list2.next.next.next.next = ListNode(17)

list3 = ListNode(2)
list3.next = ListNode(3)
list3.next.next = ListNode(5)
list3.next.next.next = ListNode(6)
list3.next.next.next.next = ListNode(8)

list4 = ListNode(4)
list4.next = ListNode(7)
list4.next.next = ListNode(13)
list4.next.next.next = ListNode(25)


sol = Solution()
print(sol.mergeKLists([list1, list2, list3, list4]))

