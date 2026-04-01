import sys
import os
import subprocess

# PyQt6 GUI components
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton


# Main application window
class FloorplannerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Input dropdown
        self.label = QLabel("Select Input File:")
        layout.addWidget(self.label)

        self.combo = QComboBox()
        input_files = self.get_input_files()
        self.combo.addItems(input_files)
        layout.addWidget(self.combo)

        # Run button
        self.button = QPushButton("Run")
        self.button.clicked.connect(self.run_placement)
        layout.addWidget(self.button)

        # Status
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.setWindowTitle('Floorplanner')
        self.show()

    # Get all JSON input files from input directory
    def get_input_files(self):
        inputs_dir = './inputs'
        files = [f for f in os.listdir(inputs_dir) if f.endswith('.json')]
        return sorted(files)

    # Run block placement
    def run_placement(self):
        selected_file = self.combo.currentText()

        # Update status 
        self.status_label.setText("Running placement")
        QApplication.processEvents()  # Forces UI to update immediately

        # Sanitize name for block placement code
        input_name = selected_file.replace('.json', '')

        # Run placement script
        cmd = ['python', 'block_placement.py', input_name]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            self.status_label.setText(f"Placement completed for {input_name}.")
            QApplication.processEvents()

            # Run visualization script
            visualize_cmd = ['python', 'visualize.py', f'{input_name}_result.json']
            subprocess.run(visualize_cmd)

            self.status_label.setText("Done.")
        else:
            # Show error output
            self.status_label.setText(f"Error: {result.stderr}")


# Gui entry
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FloorplannerGUI()
    sys.exit(app.exec())