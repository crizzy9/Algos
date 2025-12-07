from typing import Optional
# https://leetcode.com/problems/swap-nodes-in-pairs/

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # write a function that swaps every two nodes in a linked list
        # if the list is empty or has one node, return the list
        # else swap the first two nodes and recursively call the function on the rest of the list
        # return the list
        if not head or not head.next:
            return head

        head.next.next, head.next, head = head, self.swapPairs(head.next.next), head.next

        return head

if __name__ == '__main__':
    s = Solution()
    
    assert s.swapPairs(ListNode(1, ListNode(2, ListNode(3, ListNode(4))))) == ListNode(2, ListNode(1, ListNode(4, ListNode(3))))
    assert s.swapPairs(ListNode()) == ListNode()
    assert s.swapPairs(ListNode(1)) == ListNode(1)
