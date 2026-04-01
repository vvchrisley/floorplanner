import sys
import json
from random import sample
from bisect import insort

NUM_BLOCKS: int


def get_total_wire_len(wires, block_positions):
    total_len = 0
    for block1, block2, weight in wires:
        x1, y1 = block_positions[int(block1)]
        x2, y2 = block_positions[int(block2)]
        manh_dist = abs(x1 - x2) + abs(y1 - y2)
        total_len += manh_dist * weight
    return total_len


def get_abs_pos(S1, graph, widths, heights):
    '''
    Find the absolute position of every block in the current configuration
    along with the total height and width.
    '''
    pos = [[0, 0] for i in range(NUM_BLOCKS)]
    h_stacks = []
    v_stacks = []

    for idx in graph:
        curr_block = S1[idx]

        # find the longest horizontal stack this should be to the right of
        for wth, end in reversed(h_stacks):
            if end < idx:
                pos[curr_block][0] = wth
                break
        # and the tallest vertical stack it should be above
        for hgt, end in reversed(v_stacks):
            if end > idx:
                pos[curr_block][1] = hgt
                break

        # after placing a block, others can be stacked to the right or above it.
        # save the position those blocks would be inserted at, along with the index
        # so we can tell whether the graph says it should be placed there.
        x, y = pos[curr_block]
        insort(h_stacks, (x + widths[curr_block], idx))
        insort(v_stacks, (y + heights[curr_block], idx))

    # get the maximum dimensions of the entire layout
    width = h_stacks[-1][0]
    height = v_stacks[-1][0]

    return pos, width, height

def generate_initial_placement():
    block_names = range(NUM_BLOCKS)
    # generate a random sequence pair
    S0 = sample(block_names, k=NUM_BLOCKS)
    S1 = sample(block_names, k=NUM_BLOCKS)
    # constraint graph - if the graph contains the sequence [0, 2, 1], the block at
    # S1[0] is the leftmost and those at S1[2] and S1[1] are to the right of it and
    # the blocks at S1[1] and S1[0] are bottommost and the one at S1[2] is above S1[1]
    graph = [S1.index(b) for b in S0]
    return S0, S1, graph

if __name__ == '__main__':
    
    input_name = sys.argv[1]

    with open('./inputs/' + input_name + '.json') as json_file:
        floorplan = json.load(json_file)

    widths = [size[0] for size in floorplan['blocks']]
    heights = [size[1] for size in floorplan['blocks']]
    wires = floorplan['wires']

    NUM_BLOCKS = len(widths)

    S0, S1, graph = generate_initial_placement()
    positions, total_w, total_h = get_abs_pos(S1, graph, widths, heights)

    floorplan['block_positions'] = positions
    print('Area:', total_h * total_w)
    print('Wire length:', get_total_wire_len(wires, positions))

    with open(input_name + '_result.json', 'w') as f:
        json.dump(floorplan, f, indent=4)
 
    