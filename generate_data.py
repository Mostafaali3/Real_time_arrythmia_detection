import numpy as np
import matplotlib.pyplot as plt


def generate_normal_ecg(duration=10000, fs=200):
    """Generate a normal sinus rhythm ECG signal."""
    t = np.linspace(0, duration, int(duration * fs), endpoint=False)

    # Simulate normal heart rate around 70 bpm
    hr_period = 60 / 70

    # Create ECG components
    ecg = np.zeros_like(t)
    for i in range(len(t)):
        # Normal beat
        p_wave = 0.1 * np.sin(2 * np.pi * t[i] / hr_period)
        qrs_wave = 1.5 * np.exp(-((t[i] % hr_period - hr_period / 2) ** 2) / (2 * 0.1 ** 2))
        t_wave = 0.3 * np.sin(2 * np.pi * t[i] / hr_period + np.pi)

        ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.1)

    return ecg


def generate_bradycardia_ecg(duration=10000, fs=200):
    """Generate an ECG signal representing Bradycardia."""
    t = np.linspace(0, duration, int(duration * fs), endpoint=False)

    # Simulate slower heart rate around 40 bpm
    hr_period = 60 / 40

    # Create ECG components
    ecg = np.zeros_like(t)
    for i in range(len(t)):
        # Bradycardia beat
        p_wave = 0.1 * np.sin(2 * np.pi * t[i] / hr_period)
        qrs_wave = 1.5 * np.exp(-((t[i] % hr_period - hr_period / 2) ** 2) / (2 * 0.1 ** 2))
        t_wave = 0.3 * np.sin(2 * np.pi * t[i] / hr_period + np.pi)

        ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.1)

    return ecg


def generate_tachycardia_ecg(duration=10000, fs=200):
    """Generate an ECG signal representing Tachycardia."""
    t = np.linspace(0, duration, int(duration * fs), endpoint=False)

    # Simulate faster heart rate around 120 bpm
    hr_period = 60 / 120

    # Create ECG components
    ecg = np.zeros_like(t)
    for i in range(len(t)):
        # Tachycardia beat
        p_wave = 0.1 * np.sin(2 * np.pi * t[i] / hr_period)
        qrs_wave = 1.5 * np.exp(-((t[i] % hr_period - hr_period / 2) ** 2) / (2 * 0.1 ** 2))
        t_wave = 0.3 * np.sin(2 * np.pi * t[i] / hr_period + np.pi)

        ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.1)

    return ecg


def generate_pvc_ecg(duration=10000, fs=200):
    """Generate an ECG signal with Premature Ventricular Contractions (PVC)."""
    t = np.linspace(0, duration, int(duration * fs), endpoint=False)

    # Simulate normal rhythm with occasional PVCs
    hr_period = 60 / 70

    ecg = np.zeros_like(t)
    for i in range(len(t)):
        # Normal beat
        p_wave = 0.1 * np.sin(2 * np.pi * t[i] / hr_period)
        qrs_wave = 1.5 * np.exp(-((t[i] % hr_period - hr_period / 2) ** 2) / (2 * 0.1 ** 2))
        t_wave = 0.3 * np.sin(2 * np.pi * t[i] / hr_period + np.pi)

        # Insert PVC every ~3-4 beats
        if i % (int(fs * hr_period * 3.5)) == 0:
            # PVC has a different QRS complex shape
            qrs_wave = 2 * np.exp(-((t[i] % hr_period - hr_period / 2) ** 2) / (2 * 0.05 ** 2))

        ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.1)

    return ecg


def generate_pac_ecg(duration=10000, fs=200):
    """Generate an ECG signal with Premature Atrial Contractions (PAC)."""
    t = np.linspace(0, duration, int(duration * fs), endpoint=False)

    # Simulate normal rhythm with occasional PACs
    hr_period = 60 / 70

    ecg = np.zeros_like(t)
    for i in range(len(t)):
        # Normal beat
        p_wave = 0.1 * np.sin(2 * np.pi * t[i] / hr_period)
        qrs_wave = 1.5 * np.exp(-((t[i] % hr_period - hr_period / 2) ** 2) / (2 * 0.1 ** 2))
        t_wave = 0.3 * np.sin(2 * np.pi * t[i] / hr_period + np.pi)

        # Insert PAC every ~3-4 beats
        if i % (int(fs * hr_period * 3.5)) == 0:
            # PAC appears slightly earlier with a different P wave
            p_wave = 0.2 * np.sin(2 * np.pi * (t[i] + hr_period * 0.3) / hr_period)

        ecg[i] = p_wave + qrs_wave + t_wave + np.random.normal(0, 0.1)

    return ecg


# Generate and save ECG data files
ecg_types = {
    'normal_ecg.txt': generate_normal_ecg(),
    'bradycardia_ecg.txt': generate_bradycardia_ecg(),
    'tachycardia_ecg.txt': generate_tachycardia_ecg(),
    'pvc_ecg.txt': generate_pvc_ecg(),
    'pac_ecg.txt': generate_pac_ecg()
}

for filename, ecg_data in ecg_types.items():
    np.savetxt(filename, ecg_data)

    # Optional: Plot and save visualization
    plt.figure(figsize=(10, 4))
    plt.plot(ecg_data)
    plt.title(f'ECG Signal: {filename.replace("_", " ").replace(".txt", "")}')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.tight_layout()
    plt.savefig(filename.replace('.txt', '.png'))
    plt.close()

print("ECG data files and visualizations generated successfully.")