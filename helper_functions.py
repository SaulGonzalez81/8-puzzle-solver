
#A simple function to find the coordinates of an element our problem matrix
def index_loc(element,matrix):
  for i in range(len(matrix)):
    for j in range(len(matrix[i])):
      if matrix[i][j] == element:
        return i,j

#Input interface with the user. 
def prog_input():
    print("Welcome to Armie's 8-puzzle solver!")
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
        return [[1,2,3],[4,5,6],[7,8,0]]