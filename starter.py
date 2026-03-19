"""
1) Put the numbers 1-9 into a 3x3 array in random order.
2) With the goal of the numbers being in order, calculate the manhattan distance of each number from its correct position, and find the sum of all 9 distances.
3) Randomly choose two of the numbers. Determine whether swapping them would decrease the sum of distances.
4) If swapping them would decrease the total distance, accept the swap. otherwise, leave the array how it was before.
5) Repeat steps 3 & 4 until the total distance is 0.
"""



import numpy as np #used to create array
import random, math 
# 1) Put the numbers 1-9 into a 3x3 array in random order.
#Create a 3x3 array with numbers 1-9 in random order

#           0 0 0
#           0 0 0
#           0 0 0

def create_matrix(numbers):
    """
    Shuffles numbers and returns them as a 3x3 matrix.
    """
    np.random.shuffle(numbers)
    random_matrix_3x3 = numbers.reshape(3,3)
    return random_matrix_3x3
#end create_matrix

#2) With the goal of the numbers being in order, 
# calculate the manhattan distance of each number from its correct position, 
# and find the sum of all 9 distances.


#Calculate manhattan distance
#Equation: |x1 - x2| + |y1 - y2|
# x = row
# y = column

def calc_MANH_distance(matrix, n):
    """
    Calculates the manhattan distance of number n from its target position in the matrix.
    """
    target_row_formula = (n-1) // 3
    target_col_formula = (n-1) % 3
    
    current_pos = np.where(matrix == n)
    current_row = current_pos[0][0]
    current_col = current_pos[1][0]
    
    target_row = target_row_formula
    target_col = target_col_formula

    man_x = np.abs(current_row - target_row)
    man_y = np.abs(current_col - target_col)

    manh_distance = np.abs(man_x + man_y)
    
    #print(f"Current position of {n}: [{current_row}][{current_col}]")
    #print(f"Target position of {n}: [{target_row}][{target_col}]")
    
    return manh_distance
#end calc_MANH_distance


def evaluate_swap(matrix, total_manh_distance,temperature):
    """
    Evaluates whether swapping two random positions improves total manhattan distance.
    Goal is to get manhattan distance as low as possible, ideally 0.
    
    Args:
        matrix: current grid
        total_manh_distance: current total distance
        temperature: temperature for annealing, higher means more likely to accept worse solutions
        
    Returns:
        matrix: updated or reverted grid
        updated_manh_distance: new or original distance
        was_improved: True if swap was accepted, False otherwise
    """
    updated_manh_distance = 0
    updated_matrix = matrix
    old_distance = total_manh_distance
    
    
    pos1, pos2 = np.random.choice(np.arange(len(matrix.flatten())), 2, replace=False)
    #print(f"pos1: {pos1} and pos2 {pos2}")
    was_improved = False

    rows = len(matrix)
    cols = len(matrix[0])
    total_elements = rows * cols
    
    r1, c1 = divmod(pos1, cols)
    r2, c2 = divmod(pos2,cols)

    #print(r1,c1)
    #print(r2,c2)
    #print(matrix[r1,c1])
    #print(matrix[r2,c2])
    
    #performs swap
    matrix[r1][c1], matrix[r2][c2] = matrix[r2][c2], matrix[r1][c1]
   
   #gets updated manh_distance
    for i in range(1,total_elements + 1):
        man_distance = calc_MANH_distance(matrix, i)
        updated_manh_distance += man_distance
        
        #print()
        #print(f"The total manhattan distance is: {updated_manh_distance}")
        #print(f"The old distance is {old_distance}")
        
    #get delta for annealing  
    delta = updated_manh_distance - old_distance         
    
    if(random.random() < math.exp(-delta / temperature)):
        was_improved = True
    else:
        #Revert the swap if manh distance did not improve
        matrix[r1][c1], matrix[r2][c2] = matrix[r2][c2], matrix[r1][c1]
        updated_manh_distance = old_distance
    return updated_matrix, updated_manh_distance, was_improved


#simplified goal: 
# 1. Rearrange the numbers in the array in the order 1-9
# 2. Calculate the manhattan distance of each number from its correct position,
#    and find the sum of all 9 distances.

def main():
    numbers = np.arange(1,10) #creates list of numbers 1-9
    total_manh_distance = 0
    #creates the matrix:
    random_matrix_3x3 = create_matrix(numbers)
    old_random_matrix_3x3 = random_matrix_3x3.copy() #keep track of old matrix for comparison
    temperature = 100 #placeholder for temperature in annealing
    cooling_rate = 0.99 #placeholder for cooling rate in annealing
    
    #print(random_matrix_3x3)
    
    #establishes rows and cols
    rows = len(random_matrix_3x3)
    cols = len(random_matrix_3x3[0])
    total_elements = rows * cols
    
    #Calculate manhattan distance
    #Equation: |x1 - x2| + |y1 - y2|
    # |current_row - target_row| + |current_col - target_col|
    # x = row
    # y = column
    # x1 = current_row
    # x2 = target_row
    # y1 = current_col
    # y2 = target_col
    for i in range(1,total_elements + 1):
        man_distance = calc_MANH_distance(random_matrix_3x3, i)
        total_manh_distance += man_distance
        #print()
        #print(f"The manhattan distance for {i} is {man_distance}")
        #print()
        #print(f"The total manhattan distance is: {total_manh_distance}")
        
    #Swapping positions
    max_iterations = 1000
    iterations = 0
    was_improved = False
    while total_manh_distance > 0 and iterations < max_iterations:
        random_matrix_3x3, total_manh_distance, was_improved = evaluate_swap(random_matrix_3x3, total_manh_distance, temperature)
        temperature *= cooling_rate #Cool down the temperature for annealing
        iterations += 1
    if total_manh_distance == 0:
        print(f"manh distance === 0 after {iterations} iterations")
        print(f"Total temperature: {temperature}")
        print(f"Starting matrix: \n{old_random_matrix_3x3}")
        print(f"Current matrix: \n{random_matrix_3x3}")    
    else:
        print(f"Stuck at distance {total_manh_distance} after {max_iterations} iterations")
        print(f"Old matrix: \n{old_random_matrix_3x3}")
        print(f"Current matrix: \n{random_matrix_3x3}")    

#end main
    
if __name__ == '__main__':
    main()
