# main.py
# Entry point for the IC floorplanning optimizer.
# Loads JSON input, runs simulated annealing to minimize layout cost (area + wire length).
# Usage: python main.py <input_name>

import json
import block_placement
import sys
from block_placement import generate_initial_placement, get_abs_pos, get_total_wire_len
from starter import new_evaluate_swap
import math

if __name__ == '__main__':

    input_name = sys.argv[1]
    # load the JSON
    with open('./inputs/' + input_name + '.json') as json_file:
        floorplan = json.load(json_file)

    # extract data
    widths = [size[0] for size in floorplan['blocks']]
    heights = [size[1] for size in floorplan['blocks']]
    wires = floorplan['wires']

    # set NUM_BLOCKS
    block_placement.NUM_BLOCKS = len(widths)
    
    #generate initisl placement & calc initial cost
    S0, S1, graph = generate_initial_placement()
    positions, total_w, total_h = get_abs_pos(S1, graph, widths, heights)
    initial_cost = (total_w * total_h) + get_total_wire_len(wires, positions)


    
    # sample random swaps to estimate average delta
    sample_deltas = []
    S0_temp, S1_temp, graph_temp = generate_initial_placement()
    positions_temp, w_temp, h_temp = get_abs_pos(S1_temp, graph_temp, widths, heights)
    sample_cost = (w_temp * h_temp) + get_total_wire_len(wires, positions_temp)
    
    #dynamically set temperature
    #samples random swaps to estimate the average delta
    for _ in range(100):
        S0_temp, S1_temp, graph_temp, new_cost = new_evaluate_swap(
            S0_temp, S1_temp, graph_temp, widths, heights, wires, 1000, sample_cost
        )
        sample_deltas.append(abs(new_cost - sample_cost))
        sample_cost = new_cost
        
    avg_delta = sum(sample_deltas) / len(sample_deltas)
    temperature = -avg_delta / math.log(0.8)
    
    #max interations
    max_iterations = 10000
    
    min_temp = 0.01
    cooling_rate = (min_temp / temperature) ** (1 / max_iterations)
    
    #temperature = 100
    #cooling_rate = 0.99
    
    iterations = 0
    current_cost = initial_cost
    
    print(f"initial cost: {initial_cost}")
    print(f"Initial area: {total_w * total_h}")
    print(f"Initial wire length: {get_total_wire_len(wires, positions)}")
    print("-----------------------------------------")
    
    while iterations < max_iterations and temperature > 0.01:
        # call new_evaluate_swap
        S0, S1, graph, current_cost = new_evaluate_swap(S0, S1, graph, widths, heights, wires, temperature, current_cost)
        # update temperature
        temperature *= cooling_rate
        # increment iterations
        iterations += 1
        
    positions_final, final_w, final_h = get_abs_pos(S1, graph, widths, heights)
    print(f"Final area: {final_w * final_h}")
    print(f"Final wire length: {get_total_wire_len(wires, positions_final)}")
    print(f"Final cost: {current_cost}")
    print("--------------------------------------")
    print(f"Target area: {floorplan['target_area']}")
    print(f"Target wire length: {floorplan['target_wire_length']}")