# https://www.hackerrank.com/challenges/is-binary-search-tree/problem

class node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def newNode():
    temp = node(-1)
    temp.left = None
    temp.right = None
    return(temp);

""" Node is defined as
class node:
  def __init__(self, data):
      self.data = data
      self.left = None
      self.right = None
"""
def check_binary_search_tree_(root):
    res = []
    inorder_recursive(res, root)
    return sorted(res) == res and len(set(res)) == len(res)

def inorder_recursive(res, root):
    if root:
        inorder_recursive(res, root.left)
        res.append(root.data)
        inorder_recursive(res, root.right)

ht = int(input())
cnt = 0
values = map(int, input().split(' '))
values = list(values)
root  = newNode()
def inorder(root, ht):
    global cnt
    global values
    if cnt == len(values):
        return
    else:
        if(ht>0):
            root.left = newNode();
            inorder(root.left, ht-1);
        root.data = values[cnt];
        cnt+=1
        if(ht>0):
            root.right = newNode();
            inorder(root.right, ht-1);
inorder(root, ht);
if(check_binary_search_tree_(root)):
    print("Yes")
else:
    print("No")
