# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
    def printList(self):
        node = self
        while node:
            print(node.val)
            node = node.next


class Solution:
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """

        carry = 0
        ans = None
        head = None

        while l1 or l2:
            a = l1.val if l1 else 0
            b = l2.val if l2 else 0
            sum = a+b+carry
            carry = sum//10
            if not ans:
                ans = ListNode(sum%10)
                head = ans
            else:
                ans.next = ListNode(sum%10)
                ans = ans.next
            l1 = l1 and l1.next
            l2 = l2 and l2.next
        if carry:
            ans.next = ListNode(carry)
        return head


l1 = ListNode(2)
l1.next = ListNode(4)
l1.next.next = ListNode(3)

l2 = ListNode(5)
l2.next = ListNode(6)
l2.next.next = ListNode(4)

sol = Solution()
print(sol.addTwoNumbers(l1, l2).printList())

l1 = ListNode(1)
l1.next = ListNode(8)

l2 = ListNode(0)

print(sol.addTwoNumbers(l1, l2).printList())

l1 = ListNode(1)
l1.next = ListNode(8)

l2 = ListNode(9)
l2.next = ListNode(1)

print(sol.addTwoNumbers(l1, l2).printList())
