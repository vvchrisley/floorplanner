import math
import random


def get_total_wire_len(wires, block_positions):
    total_len = 0
    for block1, block2, weight in wires:
        x1, y1 = block_positions[int(block1)]
        x2, y2 = block_positions[int(block2)]
        manh_dist = abs(x1 - x2) + abs(y1 - y2)
        total_len += manh_dist * weight
    return total_len


def calc_cost(positions, widths, heights, wires):
    """
    Cost = area + wire length
    """
    max_x = 0
    max_y = 0

    for i, (x, y) in enumerate(positions):
        max_x = max(max_x, x + widths[i])
        max_y = max(max_y, y + heights[i])

    area = max_x * max_y
    wire = get_total_wire_len(wires, positions)

    return area + wire