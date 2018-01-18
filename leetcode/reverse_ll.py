class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None
    def printList(self):
        node = self
        while node:
            print(node.val)
            node = node.next


def reverse_ll(head):
    curNode = head
    prevNode = None
    while curNode.next is not None:
        nextNode = curNode.next
        curNode.next = prevNode
        prevNode = curNode
        curNode = nextNode

    curNode.next = prevNode
    curNode.printList()


head = ListNode(30)
head.next = ListNode(25)
head.next.next = ListNode(20)
head.next.next.next = ListNode(15)
head.next.next.next.next = ListNode(10)
head.next.next.next.next.next = ListNode(5)

# head.printList()

reverse_ll(head)
