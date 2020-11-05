""" tree implementation """

#the parent nodes, which point to the leaves/more parent nodes and contain the sum of the children frequencies
class ParentNode:
    def __init__(self, data):
        self.visited = 0
        self.frequency = data
        self.l = None
        self.r = None

#the leaves of the tree, which store the symbols and their respective frequencies
class Node:
    def __init__(self, data):
        self.visited = 0
        self.val = data
        self.frequency = 1
    
    def increment(self):
        self.frequency += 1
