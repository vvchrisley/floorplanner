import sys
import json
from random import sample
from bisect import insort




def get_abs_pos(S1, graph, widths, heights):
    '''
    Find the absolute position of every block in the current configuration
    along with the total height and width.
    '''
    NUM_BLOCKS = len(widths)
    pos = [[0, 0] for _ in range(NUM_BLOCKS)]
    h_stacks = []
    v_stacks = []

    for idx in graph:
        curr_block = S1[idx]

        for wth, end in reversed(h_stacks):
            if end < idx:
                pos[curr_block][0] = wth
                break

        for hgt, end in reversed(v_stacks):
            if end > idx:
                pos[curr_block][1] = hgt
                break

        x, y = pos[curr_block]
        insort(h_stacks, (x + widths[curr_block], idx))
        insort(v_stacks, (y + heights[curr_block], idx))

    width = h_stacks[-1][0] if h_stacks else 0
    height = v_stacks[-1][0] if v_stacks else 0

    return pos, width, height


def generate_initial_placement(num_blocks):
    block_names = list(range(num_blocks))

    S0 = sample(block_names, k=num_blocks)
    S1 = sample(block_names, k=num_blocks)
    graph = [S1.index(b) for b in S0]

    return S0, S1, graph