import copy
from node import Node, fN_getter
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
                sumDist = sumDist + (abs(problemIndex[0]-goalIndex[0]) + abs(problemIndex[1]-goalIndex[1]))
    return sumDist


#We calculate the value that will use to determine how close we are to the goal state and that will determine which path to take to get to the goal state the fastest
def f_n(node,option):
    if option == 1:
        return node.gN
    if option == 2:
        return node.gN + misplaced_tile_heuristic(copy.deepcopy(node))
    if option == 3:
        return node.gN + manhattan_distance_heuristic(copy.deepcopy(node)) 


#We use the f_n value stored in each node to determine their order in queue.
def queuing_function(nodes,childNodes,queuingFunctionOption):
    for i,child in enumerate(childNodes):
        child.fN = f_n(copy.deepcopy(child),queuingFunctionOption)
    if queuingFunctionOption != 1 :
        childNodes = sorted(childNodes,key=fN_getter)
    for i,val in enumerate(childNodes):
        nodes.append(val)    
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
    
    #We first create a queue to hold our nodes
    nodes = []
    nodes.append(Node(problem,0,0))
    
    #We want to continue this while loop until the length of the queue is equal to zero 
    while len(nodes) > 0:
        #We are looking at the front of the queue by popping left
        node = nodes.pop(0)

        #If the node at the front of the queue is the goal state, then we are finished and we can leave
        if node.problem == goalState:
            return node
        
        #We didn't reach the goal state, so now we call on the queuing_fucntion to push the next possible states into the queue
        nodes = queuing_function(nodes,expand(node),queuingFunctionOption)
    
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
    
    #This is a little different from the psuedocode in the book, however I find this way to be a little easier to follow given our input structure.
    result = general_search(problem,option)
    print('\n')
    if result != "failure":
        print("Depth of Solution: ", result.gN)
        for i,row in enumerate(result.problem):
            print(*row)
main_function()
