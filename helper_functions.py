#Default Puzzle Selections from depth 2 - 24
puzzle_d2 = [[1, 2, 3],[4, 5, 6],[0, 7, 8]]
puzzle_d8 = [[1, 3, 6],[5, 0, 2],[4, 7, 8]]
puzzle_d12 = [[1, 3, 6],[5, 0, 7],[4, 8, 2]]
puzzle_d16 = [[7, 1, 2],[4, 8, 5],[6, 3, 0]]
puzzle_d24 = [[0, 7, 2],[4, 6, 1],[3, 5, 8]]

#Asks the user for which default puzzle they wish to solve
def default_puzzle_selector():
  option = int(input("What level of difficultly do you want the puzzle to be (1-5): "))
  
  if option == 1:
    print("Easy Puzzle:\n")
    for i,row in enumerate(puzzle_d2):
      print(*row)
    print("\n")
    return puzzle_d2

  if option == 2:
    print("Okay Puzzle:\n")
    for i,row in enumerate(puzzle_d8):
      print(*row)
    print("\n")
    return puzzle_d8
  
  if option == 3:
    print("Kind of a Difficult Puzzle:\n")
    for i,row in enumerate(puzzle_d12):
      print(*row)
    print("\n")
    return puzzle_d12
  
  if option == 4:
    print("Difficult Puzzle:\n")
    for i,row in enumerate(puzzle_d16):
      print(*row)
    print("\n")
    return puzzle_d16
  
  if option == 5:
    print("Really Difficult Puzzle:\n")
    for i,row in enumerate(puzzle_d24):
      print(*row)
    print("\n")  
    return puzzle_d24


#A simple function to find the coordinates of an element our problem matrix
def index_loc(element,matrix):
  for i in range(len(matrix)):
    for j in range(len(matrix[i])):
      if matrix[i][j] == element:
        return i,j

#Input interface with the user. 
def prog_input():
    print("Welcome to Saul's 8-puzzle solver!")
    val = int(input("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle: "))
    while val != 1 and val != 2:
        val = int(input("Type \"1\" to use a default puzzle, or \"2\" to enter your own puzzle: "))
    if val == 2:
        print("Enter your puzzle, use a zero to represent the blank\n")
        
        userString1 = input("Enter the first row, use space between numbers: ")
        userList1 = list(userString1.split(" "))
        userList1 = list(map(int,userList1))
        print("\n")

        userString2 = input("Enter the second row, use space between numbers: ")
        userList2 = list(userString2.split(" "))
        userList2 = list(map(int,userList2))
        print("\n")
        
        userString3 = input("Enter the third row, use space between numbers: ")
        userList3 = list(userString3.split(" "))
        userList3 = list(map(int,userList3))
        print("\n")

        return [userList1,userList2,userList3]
    elif val == 1:
        return default_puzzle_selector()