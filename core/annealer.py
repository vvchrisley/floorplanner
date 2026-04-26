import random
import math
from core.placement import get_abs_pos
from core.cost import calc_cost


# based on new_evaluate_swap
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
            return self.positions, self.cost, False

        pos1, pos2 = random.sample(range(len(self.S0)), 2)

        #coin flip, choose S0 or S1
        if random.random() < 0.5:
            #S0 swap
            self.S0[pos1], self.S0[pos2] = self.S0[pos2], self.S0[pos1]
            self.graph[pos1], self.graph[pos2] = self.graph[pos2], self.graph[pos1]
            swapped_S0 = True
        else:
            #S1 swap
            self.S1[pos1], self.S1[pos2] = self.S1[pos2], self.S1[pos1]
            swapped_S0 = False
            #updated graph - swap values pos1 and pos2 wherever they appear
            for i in range(len(self.graph)):
                if self.graph[i] == pos1:
                    self.graph[i] = pos2
                elif self.graph[i] == pos2:
                    self.graph[i] = pos1

        #get new positions
        new_positions, _, _ = get_abs_pos(self.S1, self.graph, self.widths, self.heights)

        
        #calculate new cost
        new_cost = calc_cost(new_positions, self.widths, self.heights, self.wires)

        #get delta for annealing  
        delta = new_cost - self.cost
        #annealing acceptance
        accept = random.random() < math.exp(-delta / self.temperature)

        if accept:
            #Value accepted/improved
            self.positions = new_positions
            self.cost = new_cost
        else:
            #Revert the swap if manh distance did not improve
            if swapped_S0:
                #undo S0 swap
                self.S0[pos1], self.S0[pos2] = self.S0[pos2], self.S0[pos1]
                self.graph[pos1], self.graph[pos2] = self.graph[pos2], self.graph[pos1]
            else:
                #undo S1 swap
                self.S1[pos1], self.S1[pos2] = self.S1[pos2], self.S1[pos1]
                for i in range(len(self.graph)):
                    if self.graph[i] == pos1:
                        self.graph[i] = pos2
                    elif self.graph[i] == pos2:
                        self.graph[i] = pos1

        self.temperature *= self.cooling_rate
        self.iteration += 1

        return self.positions, self.cost, accept

    # Toggle Paused
    def toggle_pause(self):
        self.paused = not self.paused