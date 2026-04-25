import random
import math
from core.placement import get_abs_pos
from core.cost import calc_cost


class Annealer:
    """
    Simulated annealing engine with pause/resume control.
    """

    def __init__(self, S0, S1, graph, widths, heights, wires,
                 temperature=1000, cooling_rate=0.995):

        self.S0 = S0
        self.S1 = S1
        self.graph = graph

        self.widths = widths
        self.heights = heights
        self.wires = wires

        self.temperature = temperature
        self.cooling_rate = cooling_rate

        self.positions, _, _ = get_abs_pos(S1, graph, widths, heights)
        self.cost = calc_cost(self.positions, widths, heights, wires)

        self.paused = False
        self.iteration = 0

    def step(self):
        """
        Performs one annealing iteration.
        """

        if self.paused:
            return self.positions, self.cost

        pos1, pos2 = random.sample(range(len(self.S0)), 2)

        # swap in S0 or S1
        if random.random() < 0.5:
            self.S0[pos1], self.S0[pos2] = self.S0[pos2], self.S0[pos1]
            self.graph[pos1], self.graph[pos2] = self.graph[pos2], self.graph[pos1]
            swapped_S0 = True
        else:
            self.S1[pos1], self.S1[pos2] = self.S1[pos2], self.S1[pos1]
            swapped_S0 = False

            for i in range(len(self.graph)):
                if self.graph[i] == pos1:
                    self.graph[i] = pos2
                elif self.graph[i] == pos2:
                    self.graph[i] = pos1

        new_positions, _, _ = get_abs_pos(self.S1, self.graph, self.widths, self.heights)
        new_cost = calc_cost(new_positions, self.widths, self.heights, self.wires)

        delta = new_cost - self.cost

        accept = random.random() < math.exp(-delta / self.temperature)

        if accept:
            self.positions = new_positions
            self.cost = new_cost
        else:
            # revert swap
            if swapped_S0:
                self.S0[pos1], self.S0[pos2] = self.S0[pos2], self.S0[pos1]
                self.graph[pos1], self.graph[pos2] = self.graph[pos2], self.graph[pos1]
            else:
                self.S1[pos1], self.S1[pos2] = self.S1[pos2], self.S1[pos1]
                for i in range(len(self.graph)):
                    if self.graph[i] == pos1:
                        self.graph[i] = pos2
                    elif self.graph[i] == pos2:
                        self.graph[i] = pos1

        self.temperature *= self.cooling_rate
        self.iteration += 1

        return self.positions, self.cost

    def toggle_pause(self):
        self.paused = not self.paused