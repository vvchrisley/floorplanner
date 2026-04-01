import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys

def visualize_placement(result_file):
    # Load the result JSON
    with open(result_file, 'r') as f:
        data = json.load(f)

    positions = data['block_positions']
    widths = [block[0] for block in data['blocks']]
    heights = [block[1] for block in data['blocks']]
    wires = data['wires']

    fig, ax = plt.subplots(figsize=(10, 8))

    # Draw blocks as rectangles
    for i, (x, y) in enumerate(positions):
        rect = patches.Rectangle((x, y), widths[i], heights[i], linewidth=1, edgecolor='black', facecolor='lightblue', alpha=0.7)
        ax.add_patch(rect)
        # Label the block
        ax.text(x + widths[i]/2, y + heights[i]/2, str(i), ha='center', va='center', fontsize=8)

    # Draw wires as lines (limit to avoid clutter, or adjust)
    for block1, block2, weight in wires:
        x1, y1 = positions[int(block1)]
        x2, y2 = positions[int(block2)]
        # Center of blocks
        cx1, cy1 = x1 + widths[int(block1)]/2, y1 + heights[int(block1)]/2
        cx2, cy2 = x2 + widths[int(block2)]/2, y2 + heights[int(block2)]/2
        ax.plot([cx1, cx2], [cy1, cy2], 'r-', linewidth=0.5, alpha=0.6)

    ax.set_aspect('equal')
    ax.autoscale()
    plt.title('SoC Block Placement Visualization')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python visualize.py <result_file>")
        sys.exit(1)
    result_file = sys.argv[1]
    visualize_placement(result_file)