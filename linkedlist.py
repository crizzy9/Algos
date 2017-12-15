class Node(object):

	def __init__(self, value=None, pointer=None):
		self.value = value
		self.pointer = pointer

	def getData(self):
		return self.value

	def getNext(self):
		return self.pointer

	def setData(self, newdata):
		self.value = newdata

	def setNext(self, newpointer):
		self.pointer = newpointer


class LinkedListLIFO(object):
	def __init__(self):
		self.head = None
		self.length = 0

	# print each node's value, starting from the head
	def _printList(self):
		node = self.head
		while node:
			print(node.value)
			node = node.pointer

	# delete a node, given the previous node
	def _delete(self, prev, node):
		self.length -= 1
		if not prev:
			self.head = node.pointer
		else:
			prev.pointer = node.pointer

	# add a new node, pointing to the previous node
	# in the head
	def _add(self, value):
		self.length += 1
		self.head = Node(value, self.head)

	# locate node with some index
	def _find(self, index):
		prev = None
		node = self.head
		i = 0
		while node and i < index:
			prev = node
			node = node.pointer
			i += 1
		return node, prev, i

	# locate node by value
	def _find_by_value(self, value):
		prev = None
		node = self.head
		found = 0
		while node and not found:
			if node.value == value:
				found = True
			else:
				prev = node
				node = node.pointer
		return node, prev, found

	# find and delete a node by index
	def deleteNode(self, index):
		node, prev, i = self._find(index)
		if index == i:
			self._delete(prev, node)
		else:
			print('Node with index {} not found'.format(index))
	
	# find and delete a node by value
	def deleteNodeByValue(self, value):
		node, prev, found = self._find_by_value(value)
		if found:
			self._delete(prev, node)
		else:
			print('Node with value {} not found'.format(value))










