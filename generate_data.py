# import numpy as np
# import matplotlib.pyplot as plt
#
#
# def generate_normal_ecg(duration=10000, fs=200):
#     """Generate a normal sinus rhythm ECG signal."""
#     t = np.linspace(0, duration, int(duration * fs), endpoint=False)
#
#     # Simulate normal heart rate around 70 bpm
#     hr_period = 60 / 70
#
#     # Create ECG components
#     ecg = np.zeros_like(t)
#     for i in range(len(t)):
#         # Normal beat
#         p_wave = 0.1 * np.sin(2 * np.pi * t[i] / hr_period)
#         qrs_wave = 1.5 * np.exp(-((t[i] % hr_period - hr_period / 2) ** 2) / (2 * 0.1 ** 2))
#         t_wave = 0.3 * np.sin(2 * np.pi * t[i] / hr_period + np.pi)
#
#         ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.1)
#
#     return ecg
#
#
# def generate_bradycardia_ecg(duration=10000, fs=200):
#     """Generate an ECG signal representing Bradycardia."""
#     t = np.linspace(0, duration, int(duration * fs), endpoint=False)
#
#     # Simulate slower heart rate around 40 bpm
#     hr_period = 60 / 40
#
#     # Create ECG components
#     ecg = np.zeros_like(t)
#     for i in range(len(t)):
#         # Bradycardia beat
#         p_wave = 0.1 * np.sin(2 * np.pi * t[i] / hr_period)
#         qrs_wave = 1.5 * np.exp(-((t[i] % hr_period - hr_period / 2) ** 2) / (2 * 0.1 ** 2))
#         t_wave = 0.3 * np.sin(2 * np.pi * t[i] / hr_period + np.pi)
#
#         ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.1)
#
#     return ecg
#
#
# def generate_tachycardia_ecg(duration=10000, fs=200):
#     """Generate an ECG signal representing Tachycardia."""
#     t = np.linspace(0, duration, int(duration * fs), endpoint=False)
#
#     # Simulate faster heart rate around 120 bpm
#     hr_period = 60 / 120
#
#     # Create ECG components
#     ecg = np.zeros_like(t)
#     for i in range(len(t)):
#         # Tachycardia beat
#         p_wave = 0.1 * np.sin(2 * np.pi * t[i] / hr_period)
#         qrs_wave = 1.5 * np.exp(-((t[i] % hr_period - hr_period / 2) ** 2) / (2 * 0.1 ** 2))
#         t_wave = 0.3 * np.sin(2 * np.pi * t[i] / hr_period + np.pi)
#
#         ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.1)
#
#     return ecg
#
#
# def generate_pvc_ecg(duration=10000, fs=200):
#     """Generate an ECG signal with Premature Ventricular Contractions (PVC)."""
#     t = np.linspace(0, duration, int(duration * fs), endpoint=False)
#
#     # Simulate normal rhythm with occasional PVCs
#     hr_period = 60 / 70
#
#     ecg = np.zeros_like(t)
#     for i in range(len(t)):
#         # Normal beat
#         p_wave = 0.1 * np.sin(2 * np.pi * t[i] / hr_period)
#         qrs_wave = 1.5 * np.exp(-((t[i] % hr_period - hr_period / 2) ** 2) / (2 * 0.1 ** 2))
#         t_wave = 0.3 * np.sin(2 * np.pi * t[i] / hr_period + np.pi)
#
#         # Insert PVC every ~3-4 beats
#         if i % (int(fs * hr_period * 3.5)) == 0:
#             # PVC has a different QRS complex shape
#             qrs_wave = 2 * np.exp(-((t[i] % hr_period - hr_period / 2) ** 2) / (2 * 0.05 ** 2))
#
#         ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.1)
#
#     return ecg
#
#
# def generate_pac_ecg(duration=10000, fs=200):
#     """Generate an ECG signal with Premature Atrial Contractions (PAC)."""
#     t = np.linspace(0, duration, int(duration * fs), endpoint=False)
#
#     # Simulate normal rhythm with occasional PACs
#     hr_period = 60 / 70
#
#     ecg = np.zeros_like(t)
#     for i in range(len(t)):
#         # Normal beat
#         p_wave = 0.1 * np.sin(2 * np.pi * t[i] / hr_period)
#         qrs_wave = 1.5 * np.exp(-((t[i] % hr_period - hr_period / 2) ** 2) / (2 * 0.1 ** 2))
#         t_wave = 0.3 * np.sin(2 * np.pi * t[i] / hr_period + np.pi)
#
#         # Insert PAC every ~3-4 beats
#         if i % (int(fs * hr_period * 3.5)) == 0:
#             # PAC appears slightly earlier with a different P wave
#             p_wave = 0.2 * np.sin(2 * np.pi * (t[i] + hr_period * 0.3) / hr_period)
#
#         ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.1)
#
#     return ecg
#
#
# # Generate and save ECG data files
# ecg_types = {
#     'normal_ecg.txt': generate_normal_ecg(),
#     'bradycardia_ecg.txt': generate_bradycardia_ecg(),
#     'tachycardia_ecg.txt': generate_tachycardia_ecg(),
#     'pvc_ecg.txt': generate_pvc_ecg(),
#     'pac_ecg.txt': generate_pac_ecg()
# }
#
# for filename, ecg_data in ecg_types.items():
#     np.savetxt(filename, ecg_data)
#
#     # Optional: Plot and save visualization
#     plt.figure(figsize=(10, 4))
#     plt.plot(ecg_data)
#     plt.title(f'ECG Signal: {filename.replace("_", " ").replace(".txt", "")}')
#     plt.xlabel('Sample')
#     plt.ylabel('Amplitude')
#     plt.tight_layout()
#     plt.savefig(filename.replace('.txt', '.png'))
#     plt.close()
#
# print("ECG data files and visualizations generated successfully.")
#####################################################################################
################### bradycardia ################################################
###################################################################################
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# def generate_improved_ecg(duration=30, fs=200):
#     """
#     Generate a synthetic ECG signal with improved wave characteristics.
#
#     Args:
#     duration (float): Total duration of the ECG signal in seconds
#     fs (int): Sampling frequency in Hz
#
#     Returns:
#     numpy.ndarray: Synthetic ECG signal
#     """
#     # Create time array
#     t = np.linspace(0, duration, int(duration * fs), endpoint=False)
#
#     # Estimated parameters
#     # Slower heart rate (about 40-45 bpm)
#     hr_period = 60 / 42  # ~1.43 seconds between beats
#
#     # Initialize ECG signal
#     ecg = np.zeros_like(t)
#
#     # Create stylized ECG complex
#     for i in range(len(t)):
#         # Find the current beat cycle
#         beat_index = int(t[i] / hr_period)
#         local_time = t[i] % hr_period
#
#         # P wave - narrower, more physiological
#         if hr_period * 0.05 < local_time < hr_period * 0.15:
#             p_wave = 0.15 * np.exp(-((local_time - hr_period * 0.1) ** 2) / (2 * 0.03 ** 2))
#         else:
#             p_wave = 0
#
#         # QRS complex - much narrower and sharper
#         if hr_period * 0.2 < local_time < hr_period * 0.28:
#             qrs_wave = 1.5 * np.exp(-((local_time - hr_period * 0.24) ** 2) / (2 * 0.02 ** 2))
#         else:
#             qrs_wave = 0
#
#         # T wave - more physiological shape
#         if hr_period * 0.3 < local_time < hr_period * 0.45:
#             t_wave = 0.4 * np.exp(-((local_time - hr_period * 0.375) ** 2) / (2 * 0.05 ** 2))
#         else:
#             t_wave = 0
#
#         # Combine waves with very low noise
#         ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.01)
#
#     return ecg
#
#
# # Generate improved ECG data
# improved_ecg = generate_improved_ecg()
#
# # Save to text file
# np.savetxt('improved_ecg_signal.txt', improved_ecg)
#
# # Visualize the generated signal
# plt.figure(figsize=(15, 5))
# plt.plot(np.linspace(0, 30, len(improved_ecg)), improved_ecg, color='green', linewidth=1)
# plt.title('Synthetic Bradycardia ECG Signal (Improved)')
# plt.xlabel('Time (seconds)')
# plt.ylabel('Amplitude')
# plt.grid(True, linestyle='--', alpha=0.7)
# plt.tight_layout()
# plt.savefig('improved_ecg_signal.png', dpi=300)
# plt.close()
#
# print("Improved ECG data file and visualization generated successfully.")
#####################################################################################
################### normal ################################################
###################################################################################
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# def generate_improved_ecg(duration=30, fs=200):
#     """
#     Generate a synthetic ECG signal with more typical wave characteristics.
#
#     Args:
#     duration (float): Total duration of the ECG signal in seconds
#     fs (int): Sampling frequency in Hz
#
#     Returns:
#     numpy.ndarray: Synthetic ECG signal
#     """
#     # Create time array
#     t = np.linspace(0, duration, int(duration * fs), endpoint=False)
#
#     # Typical heart rate (about 70-75 bpm)
#     hr_period = 60 / 72  # ~0.83 seconds between beats
#
#     # Initialize ECG signal
#     ecg = np.zeros_like(t)
#
#     # Create stylized ECG complex
#     for i in range(len(t)):
#         # Find the current beat cycle
#         beat_index = int(t[i] / hr_period)
#         local_time = t[i] % hr_period
#
#         # P wave - narrower, more physiological
#         if hr_period * 0.05 < local_time < hr_period * 0.15:
#             p_wave = 0.1 * np.exp(-((local_time - hr_period * 0.1) ** 2) / (2 * 0.02 ** 2))
#         else:
#             p_wave = 0
#
#         # QRS complex - narrower and sharper, closer together
#         if hr_period * 0.2 < local_time < hr_period * 0.28:
#             qrs_wave = 1.0 * np.exp(-((local_time - hr_period * 0.24) ** 2) / (2 * 0.015 ** 2))
#         else:
#             qrs_wave = 0
#
#         # T wave - more physiological shape
#         if hr_period * 0.3 < local_time < hr_period * 0.45:
#             t_wave = 0.3 * np.exp(-((local_time - hr_period * 0.375) ** 2) / (2 * 0.04 ** 2))
#         else:
#             t_wave = 0
#
#         # Combine waves with very low noise
#         ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.01)
#
#     return ecg
#
#
# # Generate improved ECG data
# improved_ecg = generate_improved_ecg()
#
# # Save to text file
# np.savetxt('improved_ecg_signal.txt', improved_ecg)
#
# # Visualize the generated signal
# plt.figure(figsize=(15, 5))
# plt.plot(np.linspace(0, 30, len(improved_ecg)), improved_ecg, color='green', linewidth=1)
# plt.title('Synthetic Normal Sinus Rhythm ECG Signal')
# plt.xlabel('Time (seconds)')
# plt.ylabel('Amplitude')
# plt.grid(True, linestyle='--', alpha=0.7)
# plt.tight_layout()
# plt.savefig('improved_ecg_signal.png', dpi=300)
# plt.close()
#
# print("Improved ECG data file and visualization generated successfully.")
#####################################################################################
################### pac ################################################
###################################################################################

import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import matplotlib.pyplot as plt


def generate_pac_ecg(duration=30, fs=200):
    """
    Generate a synthetic ECG signal with Premature Atrial Contractions (PACs).

    Args:
    duration (float): Total duration of the ECG signal in seconds
    fs (int): Sampling frequency in Hz

    Returns:
    numpy.ndarray: Synthetic ECG signal with PACs
    numpy.ndarray: Timestamps of PAC occurrences
    """
    # Create time array
    t = np.linspace(0, duration, int(duration * fs), endpoint=False)

    # Normal sinus rhythm parameters
    normal_hr_period = 60 / 72  # ~0.83 seconds between beats (72 bpm)

    # Initialize ECG signal
    ecg = np.zeros_like(t)

    # Track PAC occurrences
    pac_timestamps = []

    # Variables for RR interval calculations
    last_beat_time = 0
    rr_intervals = []

    for i in range(len(t)):
        # Find the current beat cycle
        beat_index = int(t[i] / normal_hr_period)
        local_time = t[i] % normal_hr_period

        # Simulate PACs with specific conditions
        # PAC occurs early (reduced RR interval)
        if beat_index % 7 == 3:  # Example: PAC every 7 beats
            # PAC occurs earlier than expected
            if local_time < normal_hr_period * 0.5:
                # PAC wave characteristics
                if local_time < normal_hr_period * 0.2:
                    pac_wave = 1.2 * np.exp(-((local_time - normal_hr_period * 0.1) ** 2) / (2 * 0.02 ** 2))
                else:
                    pac_wave = 0

                # Mark PAC timestamp
                pac_timestamps.append(t[i])

                # Calculate RR intervals
                current_rr = t[i] - last_beat_time
                rr_intervals.append(current_rr)
                last_beat_time = t[i]

                # Adjusted normal beat
                if normal_hr_period * 0.2 < local_time < normal_hr_period * 0.28:
                    qrs_wave = 0.8 * np.exp(-((local_time - normal_hr_period * 0.24) ** 2) / (2 * 0.015 ** 2))
                else:
                    qrs_wave = 0

                ecg[i] = pac_wave + qrs_wave + np.random.normal(0, 0.01)
            else:
                # Normal beat generation
                # P wave
                if normal_hr_period * 0.05 < local_time < normal_hr_period * 0.15:
                    p_wave = 0.1 * np.exp(-((local_time - normal_hr_period * 0.1) ** 2) / (2 * 0.02 ** 2))
                else:
                    p_wave = 0

                # QRS complex
                if normal_hr_period * 0.2 < local_time < normal_hr_period * 0.28:
                    qrs_wave = 1.0 * np.exp(-((local_time - normal_hr_period * 0.24) ** 2) / (2 * 0.015 ** 2))
                else:
                    qrs_wave = 0

                # T wave
                if normal_hr_period * 0.3 < local_time < normal_hr_period * 0.45:
                    t_wave = 0.3 * np.exp(-((local_time - normal_hr_period * 0.375) ** 2) / (2 * 0.04 ** 2))
                else:
                    t_wave = 0

                ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.01)
        else:
            # Normal beat generation
            # P wave
            if normal_hr_period * 0.05 < local_time < normal_hr_period * 0.15:
                p_wave = 0.1 * np.exp(-((local_time - normal_hr_period * 0.1) ** 2) / (2 * 0.02 ** 2))
            else:
                p_wave = 0

            # QRS complex
            if normal_hr_period * 0.2 < local_time < normal_hr_period * 0.28:
                qrs_wave = 1.0 * np.exp(-((local_time - normal_hr_period * 0.24) ** 2) / (2 * 0.015 ** 2))
            else:
                qrs_wave = 0

            # T wave
            if normal_hr_period * 0.3 < local_time < normal_hr_period * 0.45:
                t_wave = 0.3 * np.exp(-((local_time - normal_hr_period * 0.375) ** 2) / (2 * 0.04 ** 2))
            else:
                t_wave = 0

            ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.01)

    return ecg, np.array(pac_timestamps)


# Generate PAC ECG data
pac_ecg, pac_times = generate_pac_ecg()

# Save to text file
np.savetxt('pac_ecg_signal.txt', pac_ecg)

# Visualize the generated signal
plt.figure(figsize=(15, 5))
plt.plot(np.linspace(0, 30, len(pac_ecg)), pac_ecg, color='green', linewidth=1)
plt.title('Synthetic ECG Signal with Premature Atrial Contractions')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.grid(True, linestyle='--', alpha=0.7)

# Highlight PAC occurrences
for pac_time in pac_times:
    plt.axvline(x=pac_time, color='red', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('pac_ecg_signal.png', dpi=300)
plt.close()

print(f"PAC ECG data generated with {len(pac_times)} PACs.")
print("PAC timestamps:", pac_times)

