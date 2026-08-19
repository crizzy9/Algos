from typing import Self


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val: int = 0, next: Self | None = None):
        self.val: int = val
        self.next: Self | None = next


class Solution:
    def mergeTwoLists(
        self, list1: ListNode | None, list2: ListNode | None
    ) -> ListNode | None:
        out = ListNode()
        tail = out

        while list1 is not None and list2 is not None:
            if list1.val >= list2.val:
                tail.next = list2
                list2 = list2.next
            else:
                tail.next = list1
                list1 = list1.next

            tail = tail.next

        tail.next = list1 if list1 is not None else list2

        return out.next


def print_ll(out: ListNode | None):
    out_arr: list[str] = []
    while out is not None:
        out_arr.append(str(out.val))
        out = out.next

    return "->".join(out_arr)


if __name__ == "__main__":
    s = Solution()

    l1 = ListNode(1, ListNode(2, ListNode(4)))
    l2 = ListNode(1, ListNode(3, ListNode(4)))

    k = print_ll(s.mergeTwoLists(l1, l2))
    print(k)
    assert k == "1->1->2->3->4->4"
