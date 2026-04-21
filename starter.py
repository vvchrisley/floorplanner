"""
Update 04/04/2026: starter.py now containsboth the 3x3 warmup
                   and the floorplanning optimzation


1) Put the numbers 1-9 into a 3x3 array in random order.
2) With the goal of the numbers being in order, calculate the manhattan distance of each number from its correct position, and find the sum of all 9 distances.
3) Randomly choose two of the numbers. Determine whether swapping them would decrease the sum of distances.
4) If swapping them would decrease the total distance, accept the swap. otherwise, leave the array how it was before.
5) Repeat steps 3 & 4 until the total distance is 0.
"""



import numpy as np #used to create array
import random, math
import block_placement 
from block_placement import get_abs_pos, get_total_wire_len

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
#end evaluate_swap


def new_evaluate_swap(S0, S1, graph, widths, heights, wires, temperature, old_cost):
    """
    Evaluates whether swapping two random positions in S0 or S1 improves the layout cost.
    Uses simulated annealing to occasionally accept worse swaps to avoid local minima.
    
    Args:
        S0: first sequence of the sequence pair
        S1: second sequence of the sequence pair
        graph: constraint graph derived from S0 and S1
        widths: list of block widths
        heights: list of block heights
        wires: list of wire connections [block1, block2, weight]
        temperature: current annealing temperature, higher means more likely to accept worse solutions
        old_cost: current layout cost before swap
    Returns:
        S0: updated or reverted sequence
        S1: updated or reverted sequence
        graph: updated or reverted constraint graph
        cost: new cost if swap accepted, old cost if reverted
    """
    
    pos1, pos2 = random.sample(range(len(S0)),2)
    
    swapped_S0 = False
    
    #coin flip, choose S0 or S1
    if random.random() < 0.5:
        #S0 swap
        S0[pos1], S0[pos2] = S0[pos2], S0[pos1]
        graph[pos1],graph[pos2] = graph[pos2],graph[pos1]
        swapped_S0 = True
    else:
        #S1 swap
        S1[pos1], S1[pos2] = S1[pos2], S1[pos1]
        #updated graph - swap values pos1 and pos2 wherever they appear
        for i in range(len(graph)):
            if graph[i] == pos1:
                graph[i] = pos2
            elif graph[i] == pos2:
                graph[i] = pos1
                
        
    #get new positions
    positions, total_Width, total_Height = get_abs_pos(S1, graph, widths, heights)
    
    #calculate new cost
    new_cost = (total_Width * total_Height) + get_total_wire_len(wires, positions)

    #annealing acceptance
    #get delta for annealing  
    delta = new_cost - old_cost         
    exponent = -delta / temperature
    
    if random.random() < (1.0 if exponent > 700 else math.exp(exponent)):
        #Value accepted/improved
        was_improved = True
        return S0, S1, graph, new_cost
    else:
        #Revert the swap if manh distance did not improve
        if(swapped_S0):
            #undo S0 swap
            S0[pos1], S0[pos2] = S0[pos2], S0[pos1]
            graph[pos1], graph[pos2] = graph[pos2], graph[pos1]
        else:
            #undo S1 swap
            for i in range(len(graph)):
                if graph[i] == pos2:
                    graph[i] = pos1
                elif graph[i] == pos1:
                    graph[i] = pos2
        return S0, S1, graph, old_cost   
    #print(f"pos1: {pos1} and pos2 {pos2}")

#end evaluate_swap




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