#This is the node class we will use to contain our problem space and its g(n)
class Node:
    def __init__(self,problem,gN,fN):
        self.problem = problem
        self.gN = gN
        self.fN = fN


#Getter function for fN in a node. This is used for the queuing_function
def fN_getter(Node):
    return Node.fN

#Getter function for gN in a node. This is used to break ties
def gN_getter(Node):
    return Node.gN