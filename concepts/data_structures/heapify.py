class Heapify:
    def __init__(self, data):
        self.data = data or []
        for i in range(len(data)//2, -1, -1):
            self.__max_heapify__(i)

    def __repr__(self):
        return '{}'.format(self.data)

    def parent(self, i):
        return i >> 1

    def left_child(self, i):
        return (i << 1) + 1

    def right_child(self, i):
        return (i << 1) + 2

    def __max_heapify__(self, i):
        largest = i
        left = self.left_child(i)
        right = self.right_child(i)
        n = len(self.data)
        largest = (left < n and self.data[left] > self.data[i]) and left or i
        largest = (right < n and self.data[right] > self.data[i]) and right or largest
        if i is not largest:
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            self.__max_heapify__(largest)

    def extract_max(self):
        n = len(self.data)
        max_element = self.data[0]
        self.data[0] = self.data[n-1]
        self.data = self.data[:n-1]
        self.__max_heapify__(0)
        return max_element


l = [3,2,5,1,7,8,2]
hp = Heapify(l)
print(hp)
