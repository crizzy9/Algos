
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def rotateRight(self, head: ListNode | None, k: int) -> ListNode | None:

        if not head:
            return None
        if not head.next:
            return head

        last = head
        n = 1

        while last.next is not None:
            last = last.next
            n += 1

        # print(f"last value = {last.val}")
        # print(f"len = {n}")

        knew = k % n

        if knew == 0:
            return head

        # attach last element to the first
        last.next = head

        x = 0
        cut = head
        while x != n - knew - 1:
            cut = cut.next
            x += 1

        # print(f"cut value = {cut.val}")
        # print(f"x = {x}")

        head = cut.next
        cut.next = None

        return head

if __name__ == "__main__":
    s = Solution()

    a = ListNode(1)
    a.next = ListNode(2)
    a.next.next = ListNode(3)
    a.next.next.next = ListNode(4)
    a.next.next.next.next = ListNode(5)

    o = ListNode(4)
    o.next = ListNode(5)
    o.next.next = ListNode(1)
    o.next.next.next = ListNode(2)
    o.next.next.next.next = ListNode(3)

    assert s.rotateRight(a, 5) == a
    assert s.rotateRight(a, 2) == o
    assert s.rotateRight(a, 4) == o
