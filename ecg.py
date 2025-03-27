import sys
import numpy as np
# from pyqtgraph.examples.VideoSpeedTest import iterations_counter
from scipy.signal import find_peaks
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QMessageBox, QLabel, QFileDialog, QHBoxLayout)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtCore import Qt
import pyqtgraph as pg


class ECGApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.ecg_data = None
        self.fs = 200  # Default sampling rate (Hz)
        self.current_index = 0
        self.plot_interval = 0.2  # seconds per update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.current_file = ""
        
        # Data for plotting
        self.x = []  # time values in seconds
        self.y = []  # ECG amplitude
        
        # For arrhythmia detection (using RR intervals and QRS widths)
        self.rr_intervals = []  # list of detected RR intervals (in seconds)
        self.qrs_widths = []    # corresponding QRS widths (in seconds)

        #plotting -talal
        self.window_size = 500
        # Fixed and updated initialization
        self.fixedX = np.linspace(0, (self.window_size - 1) / self.fs, self.window_size)
        self.plottedY = np.zeros(self.window_size)
        self.plot_curve = self.plot_widget.plot(self.fixedX, self.plottedY, pen=pg.mkPen(color="lime", width=2))


        self.index = 0
        # self.plot_curve = self.plot_widget.plot(self.x, self.y, pen=pg.mkPen(color="lime", width=2))

        # Track which abnormal condition has already triggered an alert
        self.alerted_conditions = set()
        self.alert_iterations = 0  # Counter for keeping alert longer
        self.alert_duration = 300
    def initUI(self):
        self.setWindowTitle('ECG Analysis')
        self.setStyleSheet("QMainWindow { color: white; background-color: #1A1A1A; }")
        self.setGeometry(50, 50, 1400, 800)
        # self.setStyleSheet("background-color:  #1A1A1A ;")


        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('left', 'Amplitude')
        self.plot_widget.setLabel('bottom', 'Time (s)')
        self.plot_widget.setYRange(-3, 3)
        self.plot_widget.showGrid(x=True, y=False)
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.getAxis("left").setVisible(False)
        self.plot_widget.getAxis("bottom").setVisible(False)
        self.plot_widget.setBackground('#1A1A1A')
        self.plot_curve = self.plot_widget.plot()


        self.heartRateLabel = QLabel("HR (bpm)")
        self.heartRateValLabel = QLabel("000")
        self.heartRateValLabel.setFixedWidth(int(self.width()*3/20))

        self.heartRateLabel.setStyleSheet("""
                                            color: Lime;
                                            font-size: 14px;
                                            font-weight: bold;
                                            """)
        self.heartRateLabel.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.heartRateValLabel.setStyleSheet("""
                                            margin-top: 2px;
                                            color: Lime;
                                            font-size: 100px;
                                            font-weight: bold;
                                            """)
        self.heartRateValLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("Status: Ready")
        self.file_label = QLabel("No file selected")

        self.file_label.setStyleSheet("""
                                 color: white;
                                 font-size: 12px;
                                 font-weight: bold;
                                  """)
        
        # Buttons
        self.load_btn = QPushButton("Load")
        self.load_btn.clicked.connect(self.load_file)
        self.start_btn = QPushButton("Start \nAnalysis")
        self.start_btn.clicked.connect(self.start_analysis)
        self.start_btn.setEnabled(False)

        self.start_btn.setStyleSheet("""
                                    background-color:  white;
                                    font-weight: bold;
                                    """)
        self.load_btn.setStyleSheet("""
                                    background-color:  white;
                                    font-weight: bold;
                                    """)

        self.start_btn.setFixedSize(70,70)
        self.load_btn.setFixedSize(70,70)

        self.createAlertPanel()
        self.setupLayout()

    def createAlertPanel(self):
        self.alertLabel = QLabel("Normal")
        self.alertLabel.setStyleSheet("""
            margin-left: 20px;
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        self.alertLabel.setFixedHeight(40)
        self.alertLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.alertLED1 = QPushButton()
        self.alertLED2 = QPushButton()
        self.alertLED3 = QPushButton()

        style = """
            background-color:  #00bcd4;
            border-top-left-radius: 10px;
            border-bottom-right-radius: 10px;
            border: none;
        """

        for btn in [self.alertLED1, self.alertLED2, self.alertLED3]:
            btn.setStyleSheet(style)
            btn.setFixedSize(120, 20)
            btn.setEnabled(False)

    def setupLayout(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20,20,20,20)

        alertPanelLayout = QHBoxLayout()
        alertPanelLayout.addWidget(self.alertLED1)
        alertPanelLayout.addWidget(self.alertLED2)
        alertPanelLayout.addWidget(self.alertLED3)
        alertPanelLayout.addWidget(self.alertLabel)
        alertPanelLayout.addStretch()

        heartRateLayout = QVBoxLayout()
        heartRateLayout.addStretch()
        heartRateLayout.addWidget(self.heartRateLabel)
        heartRateLayout.addWidget(self.heartRateValLabel)
        heartRateLayout.addStretch()

        monitorLayout = QHBoxLayout()
        monitorLayout.addWidget(self.plot_widget)
        monitorLayout.addLayout(heartRateLayout)

        # layout.addWidget(self.plot_widget)
        # layout.addWidget(self.status_label)
        # layout.addWidget(self.file_label)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.load_btn)
        buttonsLayout.addWidget(self.start_btn)
        buttonsLayout.addWidget(self.file_label)
        buttonsLayout.addStretch()

        # layout.addWidget(self.load_btn)
        # layout.addWidget(self.start_btn)

        layout.addLayout(alertPanelLayout,10)
        layout.addLayout(monitorLayout,80)
        layout.addLayout(buttonsLayout,10)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_file(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Select ECG Data File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if fileName:
            try:
                self.ecg_data = np.loadtxt(fileName)
                self.current_file = fileName
                self.file_label.setText(f"Loaded: {fileName.split('/')[-1]}")
                self.status_label.setText("Status: File loaded successfully")
                self.start_btn.setEnabled(True)
                self.reset_analysis()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
                self.start_btn.setEnabled(False)

    def reset_analysis(self):
        self.current_index = 0
        self.x = []
        self.y = []
        self.plot_curve.clear()
        self.rr_intervals = []
        self.qrs_widths = []
        self.alerted_conditions.clear()
        if self.timer.isActive():
            self.timer.stop()

    def start_analysis(self):
        if self.ecg_data is None:
            QMessageBox.warning(self, "Warning", "Please load a file first")
            return

        self.reset_analysis()
        self.start_btn.setEnabled(False)
        self.status_label.setText("Status: Starting analysis...")
        
        try:
            # self.timer.start(int(self.plot_interval * 200))
            # self.timer.start(2000)
            self.timer.start(int(1 / self.fs * 1000))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to start analysis: {str(e)}")
            self.start_btn.setEnabled(True)

    def update_plot(self):
        # End-of-data check
        if self.current_index >= len(self.ecg_data):
            self.timer.stop()
            self.final_diagnosis()
            # self.status_label.setText("Analysis complete")
            self.alertLabel.setText("Analysis complete")
            self.start_btn.setEnabled(True)
            return

        # Process one chunk
        chunk_size = int(self.fs * self.plot_interval)
        end_idx = min(self.current_index + chunk_size, len(self.ecg_data))
        new_x = np.arange(self.current_index, end_idx) / self.fs
        new_y = self.ecg_data[self.current_index:end_idx]
        self.x.extend(new_x.tolist())
        self.y.extend(new_y.tolist())

        #Plotting Patiet Monitor Update and data

        if self.index < len(self.ecg_data):
            pos = self.index % self.window_size  # Get position in fixed window
            self.plottedY[pos] = self.ecg_data[self.index]  # Insert new ECG value

            #OFFSET
            for i in range(1, 20):
                if pos + i < self.window_size:
                    self.plottedY[pos + i] = np.nan

            self.index += 1

        self.plot_curve.setData(self.fixedX, self.plottedY, connect="finite")  # Update graph


        # Slide window on x-axis
        # if self.x[-1] > 5:
        #     self.plot_widget.setXRange(self.x[-1] - 5, self.x[-1])
        # else:
        #     self.plot_widget.setXRange(0, 5)

        # Use entire data so far for peak detection and heart rate estimation
        ## remove fluctuations
        data_so_far = np.array(self.y)
        threshold = np.mean(data_so_far) + np.std(data_so_far)
        # peaks, _ = find_peaks(data_so_far, height=threshold, distance=self.fs//2)
        # if len(peaks) > 1:
        #     # Compute instantaneous heart rate based on latest RR
        #     inst_hr = 60 / latest_rr
        # In update_plot method, replace heart rate calculation with:
        peaks, _ = find_peaks(data_so_far, height=threshold, distance=self.fs // 2)
        if len(peaks) > 2:
            inst_hr = self.calculate_stable_heart_rate(peaks, self.fs)
            self.heartRateValLabel.setText(f"{inst_hr:.0f}")
            # Compute latest RR interval from the last two peaks
            latest_rr = (peaks[-1] - peaks[-2]) / self.fs
            self.rr_intervals.append(latest_rr)

            # Update status label with heart rate and latest RR
            # self.status_label.setText(
            #     f"Heart Rate: {inst_hr:.1f} bpm | Latest RR: {latest_rr:.3f}s"
            # )


            self.heartRateValLabel.setText(f"{inst_hr:.0f}")

            # For the current chunk, perform simplified QRS width estimation:
            # Here we take the segment between the last two peaks.
            start_seg = peaks[-2]
            end_seg = peaks[-1]
            segment = data_so_far[start_seg:end_seg]
            qrs_width = self.calculate_qrs_width(segment)
            self.qrs_widths.append(qrs_width)
            if len(self.rr_intervals) > 8:
                self.rr_intervals = self.rr_intervals[-8:]
                self.qrs_widths = self.qrs_widths[-8:]
            
            # Analyze the current condition based on RR intervals and QRS widths
            condition = self.analyze_current_condition()
            # self.status_label.setText(
            #     f"Heart Rate: {inst_hr:.1f} bpm | Condition: {condition}"
            # )
            self.heartRateValLabel.setText(f"{inst_hr:.0f}")



            # Show alert if condition is abnormal and not already alerted
            # if condition != "Normal" and condition not in self.alerted_conditions:
            #     # self.alerted_conditions.add(condition)
            #     # self.show_alert(condition, inst_hr)
            #     iterationsAfterAlert = 0
            #
            #     style = """
            #                 background-color:  #Red;
            #                 border-top-left-radius: 10px;
            #                 border-bottom-right-radius: 10px;
            #                 border: none;
            #             """
            # else:
            #     style = """
            #                 background-color:  #00bcd4;
            #                 border-top-left-radius: 10px;
            #                 border-bottom-right-radius: 10px;
            #                 border: none;
            #             """
            #
            # for btn in [self.alertLED1, self.alertLED2, self.alertLED3]:
            #         btn.setStyleSheet(style)

            # Keep the alert ON for a set number of iterations
            print(f"Condition detected: {condition}")

            if condition != "Normal":
                self.alerted_conditions.add(condition)
                self.alert_iterations = self.alert_duration  # Reset counter
                # set text to the last element in the alerted condition set
                self.alertLabel.setText(condition)
                # self.show_alert(condition, inst_hr)

            # Decrease counter every iteration
            if self.alert_iterations > 0:
                style = """
                            background-color: #ff0000; /* Red */
                            border-top-left-radius: 10px;
                            border-bottom-right-radius: 10px;
                            border: none;
                        """
                self.alert_iterations -= 1  # Countdown
            else:
                self.alertLabel.setText("Normal")
                style = """
                            background-color: #00bcd4; /* Default */
                            border-top-left-radius: 10px;
                            border-bottom-right-radius: 10px;
                            border: none;
                        """

            for btn in [self.alertLED1, self.alertLED2, self.alertLED3]:
                btn.setStyleSheet(style)

        self.current_index = end_idx

    def calculate_stable_heart_rate(self, peaks, sampling_rate):
        """
        Calculate a more stable heart rate using multiple RR intervals.

        Args:
            peaks (numpy.ndarray): Array of peak indices
            sampling_rate (float): Sampling frequency of the signal

        Returns:
            float: Stable heart rate in beats per minute
        """
        if len(peaks) < 3:
            return 0

        # Calculate RR intervals
        rr_intervals = np.diff(peaks) / sampling_rate

        # Remove outliers (RR intervals more than 1.5 times the interquartile range)
        q1, q3 = np.percentile(rr_intervals, [25, 75])
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        filtered_intervals = rr_intervals[
            (rr_intervals >= lower_bound) &
            (rr_intervals <= upper_bound)
            ]

        # Calculate heart rate from filtered intervals
        if len(filtered_intervals) > 0:
            avg_rr_interval = np.mean(filtered_intervals)
            heart_rate = 60 / avg_rr_interval
            return heart_rate

        return 0

    def calculate_heart_rate(self, signal):
        # Compute heart rate from peaks in the given signal
        try:
            threshold = np.mean(signal) + np.std(signal)
            peaks, _ = find_peaks(signal, height=threshold, distance=self.fs//2)
            if len(peaks) > 1:
                rr_intervals = np.diff(peaks) / self.fs
                heart_rate = 60 / np.mean(rr_intervals)
                return heart_rate
            return 0
        except Exception:
            return 0

    def calculate_qrs_width(self, signal):
        # Simplified QRS width calculation:
        # Determine indices where signal exceeds threshold
        threshold = np.mean(signal) + 0.5 * np.std(signal)
        indices = np.where(signal > threshold)[0]
        if len(indices) > 1:
            return (indices[-1] - indices[0]) / self.fs
        return 0

    def analyze_current_condition(self):
        # Need at least 8 RR intervals and one QRS width measurement
        if len(self.rr_intervals) < 8 or len(self.qrs_widths) == 0:
            return "Analyzing..."
        
        RRn = self.rr_intervals[-1]   # Latest RR interval
        Wn = self.qrs_widths[-1]        # Latest QRS width
        ARn = np.mean(self.rr_intervals[-8:])  # Average RR over last 8 intervals
        prev_rr = self.rr_intervals[-2] if len(self.rr_intervals) > 1 else RRn

        # Apply detection criteria (tolerance of 0.1s)
        if RRn > 1.5 or ARn > 1.2:
            return "Bradycardia"
        if ARn < 0.6:
            return "Tachycardia"
        if RRn < 0.875 * ARn and Wn > 0.12 and abs(prev_rr + RRn - 2 * ARn) <= 0.1:
            return "PVC"
        if RRn < 0.875 * ARn and Wn <= 0.12 and (prev_rr + RRn) < 2 * ARn - 0.1:
            return "PAC"
        return "Normal"

    def show_alert(self, condition, hr):
        alert = QMessageBox(self)
        alert.setIcon(QMessageBox.Icon.Warning)
        alert.setWindowTitle("ECG Alert")
        alert.setText(f"Alert: {condition} detected\nHeart Rate: {hr:.1f} bpm")
        alert.setStandardButtons(QMessageBox.StandardButton.Ok)
        # Use exec() to show a modal alert
        alert.exec()

    def final_diagnosis(self):
        if self.ecg_data is None or self.fs == 0:
            QMessageBox.warning(self, "Warning", "No ECG data available for diagnosis")
            return

        try:
            threshold = np.mean(self.ecg_data) + np.std(self.ecg_data)
            peaks, _ = find_peaks(self.ecg_data, height=threshold, distance=self.fs//2)
            if len(peaks) < 2:
                QMessageBox.information(self, "Final Diagnosis", "Not enough data for diagnosis")
                return
            rr_intervals = np.diff(peaks) / self.fs

            diagnosis = []
            if np.mean(rr_intervals) > 1.5:
                diagnosis.append("Bradycardia")
            if np.mean(rr_intervals) < 0.6:
                diagnosis.append("Tachycardia")
            diag_text = f"Average Heart Rate: {60/np.mean(rr_intervals):.1f} bpm\n"
            if diagnosis:
                diag_text += "Finished diagnosis:\n" 
            else:
                diag_text += "Finished diagnosis:\n" 
                
            final_msg = QMessageBox(self)
            final_msg.setIcon(QMessageBox.Icon.Information)
            final_msg.setWindowTitle("Final Diagnosis")
            final_msg.setText(diag_text)
            final_msg.exec()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Diagnosis failed: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ECGApp()
    ex.show()
    sys.exit(app.exec())
