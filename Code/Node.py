class Node:
    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        self.sample = -1
        self.feature = -1
    def __copy__(self):
        node = Node()
        node.left = self.left
        node.right = self.right
        node.sample = self.sample
        node.feature = self.feature
        node.parent = self.parent
        return node