import sys
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer
import pyqtgraph as pg


class ECGMonitor(QWidget):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.setWindowTitle("Real-Time ECG Monitor")
        self.setGeometry(100, 100, 800, 400)

        # Layout for ECG Graph
        layout = QVBoxLayout()
        self.setLayout(layout)

        # ECG Graph Setup
        self.graphWidget = pg.PlotWidget()
        layout.addWidget(self.graphWidget)

        self.graphWidget.setBackground("black")
        self.graphWidget.showGrid(x=True, y=True)

        # **Hide Axes**
        self.graphWidget.getAxis("left").setVisible(False)
        self.graphWidget.getAxis("bottom").setVisible(False)

        # ECG Data Configuration (Simulated ECG Waveform)
        t = np.linspace(0, 2 * np.pi, 5000)
        self.ecg_data = (np.sin(t) + 0.5 * np.sin(600 * t) + 0.2 * np.sin(1000 * t)) * 1.2
        self.ecg_data = self.ecg_data / np.max(np.abs(self.ecg_data))  # Normalize to [-1, 1]
        self.graphWidget.setYRange(np.min(self.ecg_data), np.max(self.ecg_data))

        self.window_size = 50  # Fixed x-axis window size
        self.x = np.arange(self.window_size)  # Fixed x-axis
        self.y = np.zeros(self.window_size)  # Initial y-values

        self.index = 0  # Tracks where to insert new values
        self.curve = self.graphWidget.plot(self.x, self.y, pen=pg.mkPen(color="lime", width=2))

        # Timer for Real-Time Update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)  # Update every 100ms

    def update_plot(self):
        if self.index < len(self.ecg_data):
            pos = self.index % self.window_size  # Get position in fixed window
            self.y[pos] = self.ecg_data[self.index]  # Insert new ECG value

            # Apply the "offset replacement" logic (clearing older values gradually)
            for i in range(1, 2):
                if pos + i < self.window_size:
                    self.y[pos + i] = np.nan  # Simulate missing points as per your pattern

            self.index += 1  # Move to next ECG point

        self.curve.setData(self.x, self.y, connect="finite")  # Update graph


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ECGMonitor()
    window.show()
    sys.exit(app.exec())
