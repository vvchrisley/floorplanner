import sys
import json

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QComboBox, QCheckBox, QSpinBox
)
from PyQt6.QtCore import QTimer

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from core.placement import generate_initial_placement
from core.annealer import Annealer


class FloorplannerGUI(QWidget):

    def __init__(self):
        super().__init__()

        self.annealer = None
        self.widths = None
        self.heights = None
        self.wires = None

        self.max_iterations = 10000

        self.initial_temp = None

        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(30)

    def init_ui(self):
        layout = QVBoxLayout()

        # File selection
        layout.addWidget(QLabel("Select Input File"))

        self.combo = QComboBox()
        self.combo.addItems(self.get_inputs())
        layout.addWidget(self.combo)

        # Iteration control
        layout.addWidget(QLabel("Max Iterations"))

        self.iter_input = QSpinBox()
        self.iter_input.setRange(1, 1_000_000)
        self.iter_input.setValue(10000)
        layout.addWidget(self.iter_input)

        # Wire toggle
        self.wire_checkbox = QCheckBox("Show Wires")
        self.wire_checkbox.setChecked(True)
        layout.addWidget(self.wire_checkbox)

        # Buttons
        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.start)
        layout.addWidget(self.start_btn)

        self.pause_btn = QPushButton("Pause / Resume")
        self.pause_btn.clicked.connect(self.pause)
        layout.addWidget(self.pause_btn)

        # Status
        self.status = QLabel("")
        layout.addWidget(self.status)

        # Plot
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.setWindowTitle("Floorplanner")

    def get_inputs(self):
        import os
        return sorted(f for f in os.listdir("./inputs") if f.endswith(".json"))

    def start(self):
        file = self.combo.currentText().replace(".json", "")

        with open(f"./inputs/{file}.json") as f:
            data = json.load(f)

        self.widths = [b[0] for b in data["blocks"]]
        self.heights = [b[1] for b in data["blocks"]]
        self.wires = data["wires"]

        self.max_iterations = self.iter_input.value()

        num_blocks = len(self.widths)
        S0, S1, graph = generate_initial_placement(num_blocks)

        self.annealer = Annealer(S0, S1, graph, self.widths, self.heights, self.wires)

        self.initial_temp = getattr(self.annealer, "temperature", 1.0)


    def pause(self):
        if self.annealer:
            self.annealer.toggle_pause()

    def update_simulation(self):
        if not self.annealer:
            return

        # stop at max iterations
        if self.annealer.iteration >= self.max_iterations:
            self.status.setText(f"Done at iter {self.annealer.iteration}")
            return

        pos, cost = self.annealer.step()

        temp = getattr(self.annealer, "temperature", None)

        # normalize temperature for finding rgb
        if temp is not None and self.initial_temp:
            t_norm = max(0.0, min(1.0, temp / self.initial_temp))
        else:
            t_norm = 0.0

        # calculate rgb
        r = int(255 * t_norm)
        b = int(255 * (1 - t_norm))
        g = 0

        self.status.setText(
            f"Cost: {cost:.2f} | Iter: {self.annealer.iteration} | Temp: {temp:.4f}"
        )

        # assign color
        self.status.setStyleSheet(
            f"color: rgb({r}, {g}, {b});"
        )

        self.draw(pos)

    def draw(self, positions):
        self.ax.clear()

        # draw blocks
        for i, (x, y) in enumerate(positions):
            w = self.widths[i]
            h = self.heights[i]

            rect = plt.Rectangle((x, y), w, h, alpha=0.6)
            self.ax.add_patch(rect)

            self.ax.text(
                x + w / 2,
                y + h / 2,
                str(i),
                ha='center',
                va='center',
                fontsize=8
            )

        # draw wires
        if self.wire_checkbox.isChecked():
            for block1, block2, weight in self.wires:
                x1, y1 = positions[int(block1)]
                x2, y2 = positions[int(block2)]

                cx1 = x1 + self.widths[int(block1)] / 2
                cy1 = y1 + self.heights[int(block1)] / 2
                cx2 = x2 + self.widths[int(block2)] / 2
                cy2 = y2 + self.heights[int(block2)] / 2

                self.ax.plot([cx1, cx2], [cy1, cy2], linewidth=0.5, alpha=0.6)

        self.ax.set_aspect("equal")
        self.ax.grid(True, alpha=0.3)

        self.ax.relim()
        self.ax.autoscale_view()

        self.canvas.draw()


# Entry point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FloorplannerGUI()
    window.show()
    sys.exit(app.exec())