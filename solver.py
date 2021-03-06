import time
import copy
from node import Node, fN_getter, gN_getter
from helper_functions import index_loc, prog_input 

#This is a global goal state that we will be used to check if a search has reached the goal state
goalState = [[1,2,3],[4,5,6],[7,8,0]]


#We compare our problem state with the goal state and count how many differneces there are
def misplaced_tile_heuristic(node):
    misplaced = 0
    for i,row in enumerate(node.problem):
        for j,val in enumerate(row):
            if val != goalState[i][j]:
                misplaced = misplaced + 1
    return misplaced


#We compare our problem state with the goal state and calculate the mahattan distance for each tile in the problem state and add them up.
def manhattan_distance_heuristic(node):
    sumDist = 0
    for i,row in enumerate(node.problem):
        for j,val in enumerate(row):
            if val != 0:
                problemIndex = index_loc(val,node.problem)
                goalIndex = index_loc(val,goalState)
                manDist = (abs(problemIndex[0]-goalIndex[0]) + abs(problemIndex[1]-goalIndex[1]))
                sumDist = sumDist + manDist
    return sumDist


#We calculate the value that will use to determine how close we are to the goal state and that will determine which path to take to get to the goal state the fastest
def f_n(node,option):
    if option == 1:
        return node.gN
    if option == 2:
        return node.gN + misplaced_tile_heuristic(copy.deepcopy(node))
    if option == 3:
        return node.gN + manhattan_distance_heuristic(copy.deepcopy(node)) 


#We use the f_n value stored in each node to determine their order in queue. We sort the queue when we do Misplaced tiles and Manhattan distance and break ties that could occur
def queuing_function(nodes,childNodes,queuingFunctionOption,dupes):
    
    for i,val in enumerate(dupes):
        for j,val2 in enumerate(childNodes):
            if val.problem == val2.problem:
                childNodes.remove(val2)

    for i,child in enumerate(childNodes):
        child.fN = f_n(copy.deepcopy(child),queuingFunctionOption)

    for i,val in enumerate(childNodes):
        dupes.append(val)
    
    for i,val in enumerate(childNodes):
        nodes.append(val) 
    
    #Sort and break ties if they occur
    if queuingFunctionOption != 1 :
        nodes = sorted(nodes,key= fN_getter)
        tieNode = nodes.pop(0)
        tieNodes = [tieNode]
        for i,val in enumerate(nodes):
            if val.fN == tieNode.fN:
                tieNodes.append(val)
                nodes.remove(val)
        tieNodes = sorted(tieNodes,key= gN_getter)
        for i, val in enumerate(nodes):
            tieNodes.append(val)
        return tieNodes
    else:
        return nodes


#We create child nodes from our given node based on the legal operators that we can use to change the board state
def expand(node):
    #(len(node.problem[0]))
    childNodes = []
    blankSpaceLoc = index_loc(0,node.problem) 

    #Check if moving the blank tile up works
    if 0 <= (blankSpaceLoc[0] - 1):
        cnode1 = copy.deepcopy(node)
        tmp = cnode1.problem[blankSpaceLoc[0]][blankSpaceLoc[1]]
        cnode1.problem[blankSpaceLoc[0]][blankSpaceLoc[1]] = cnode1.problem[blankSpaceLoc[0]-1][blankSpaceLoc[1]]
        cnode1.problem[blankSpaceLoc[0]-1][blankSpaceLoc[1]] = tmp
        cnode1.gN = cnode1.gN + 1
        childNodes.append(cnode1)        

    #Check if moving the blank tile down works
    if (blankSpaceLoc[0] + 1) < (len(node.problem[0])):
        cnode2 = copy.deepcopy(node)
        tmp = cnode2.problem[blankSpaceLoc[0]][blankSpaceLoc[1]]
        cnode2.problem[blankSpaceLoc[0]][blankSpaceLoc[1]] = cnode2.problem[blankSpaceLoc[0]+1][blankSpaceLoc[1]]
        cnode2.problem[blankSpaceLoc[0]+1][blankSpaceLoc[1]] = tmp
        cnode2.gN = cnode2.gN + 1
        childNodes.append(cnode2)
    
    #Check if moving the blank tile left works
    if 0 <= (blankSpaceLoc[1] - 1):
        cnode3 = copy.deepcopy(node)
        tmp = cnode3.problem[blankSpaceLoc[0]][blankSpaceLoc[1]]
        cnode3.problem[blankSpaceLoc[0]][blankSpaceLoc[1]] = cnode3.problem[blankSpaceLoc[0]][blankSpaceLoc[1]-1]
        cnode3.problem[blankSpaceLoc[0]][blankSpaceLoc[1]-1] = tmp
        cnode3.gN = cnode3.gN + 1
        childNodes.append(cnode3)
    
    #Check if moving the blank tile right works
    if (blankSpaceLoc[1] + 1) < (len(node.problem[0])):
        cnode4 = copy.deepcopy(node)
        tmp = cnode4.problem[blankSpaceLoc[0]][blankSpaceLoc[1]]
        cnode4.problem[blankSpaceLoc[0]][blankSpaceLoc[1]] = cnode4.problem[blankSpaceLoc[0]][blankSpaceLoc[1]+1]
        cnode4.problem[blankSpaceLoc[0]][blankSpaceLoc[1]+1] = tmp
        cnode4.gN = cnode4.gN + 1
        childNodes.append(cnode4)
    return childNodes

#This is where we will perform our search using the algorithm that the user desires 
def general_search(problem,queuingFunctionOption):
    
    #We first create a queue to hold our nodes & another queue to hold our duplicate nodes
    nodes = []
    nodes_dups = []
    nodes.append(Node(problem,0,0))
    #nodes_dups.append(Node(problem,0,0))

    #These variables are going to be used to keep track of the maximum queue size and the amount of nodes we have expanded.
    global maxQueueSize
    maxQueueSize = 1
    global totalExpandedNodes
    totalExpandedNodes = 0

    #We want to continue this while loop until the length of the queue is equal to zero 
    while len(nodes) > 0:
        #We are looking at the front of the queue by popping left
        node = nodes.pop(0)

        #If the node at the front of the queue is the goal state, then we are finished and we can leave
        if node.problem == goalState:
            print("We reached the goal state!\n")
            for i, row in enumerate(node.problem):
                print(*row)
            print("\n")
            return node

        #We didn't reach the goal state, so now we call on the queuing_fucntion to push the next possible states into the queue
        nodes = queuing_function(nodes,expand(node),queuingFunctionOption,nodes_dups)
        
        #Print out of the node we are expanding
        hN = node.fN - node.gN
        print("The best state to expand with a g(n) =",node.gN, "and h(n) =", hN, "is..\n" )
        for i,row in enumerate(node.problem):
            print(*row) 
        print('\n')
        
        #Keeps track of how many nodes we hae expanded
        totalExpandedNodes = totalExpandedNodes + 1
        
        #Keeps track of the maxQueueSize
        if len(nodes) >= maxQueueSize:
            maxQueueSize = len(nodes)

    #If we go through the entire queue without reaching the goal state, we can call this a failure
    return "failure"


#This is going to be the main "driver" for the program where we recieve input from the user and perform our search.
def main_function():
    #We use a function to grab the input from the user and return in a usuable format
    problem = prog_input()

    #Now we are recieving the user's choice of alogirthm and that will determine what kind of heuristic we will use in our general search
    option = int(input("Enter your choice of algorithm\n1. Uniform Cost Search.\n2. A* with the Misplaced Tile heuristic.\n3. A* with the Manhattan distance heuristic.\n"))
    while option != 1 and option != 2 and option != 3:
        option = int(input("Enter your choice of alogirthm\n1. Uniform Cost Search.\n2. A* with the Misplaced Tile heuristic.\n3. A* with the Manhattan distance heuristic.\n"))
    print('\n')

    #This is a little different from the psuedocode in the book, however I find this general search to be a little easier to follow given my input structure.
    tStart = time.time()
    result = general_search(problem,option)
    tEnd = time.time()

    #This totalTime calculates how much time has passed since we started the general_search.
    totalTime = tEnd - tStart
    
    if result != "failure":
        print("Time Elapsed", totalTime, "seconds")
        print("The search expanded a total of", totalExpandedNodes, "nodes")
        print("The maximum number of nodes in the queue at any one time was", maxQueueSize)
        print("The depth of goal state was", result.gN, "\n")
    else:
        print("failure")
main_function()
