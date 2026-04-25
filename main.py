import sys
from PyQt6.QtWidgets import QApplication
from gui import FloorplannerGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FloorplannerGUI()
    window.show()
    sys.exit(app.exec())