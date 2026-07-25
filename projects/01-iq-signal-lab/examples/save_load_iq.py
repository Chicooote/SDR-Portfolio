from iq_playground.signal_generator import generate_complex_tone
from sdr_core.io.iq import load_iq, save_iq

# Generate a 100 kHz complex sinusoid
# sampled at 1 MHz
fs = 1_000_000
f = 100_000
N = 1000
iq = generate_complex_tone(fs, f, N)

file_path = "01-iq-signal-lab/data/tone_100khz.npy"

# Save IQ samples
save_iq(iq, file_path)

# Load IQ samples (no metadata sidecar was saved for this simulated signal)
loaded_signal, _ = load_iq(file_path)

print(f"Original samples : {iq.shape}")
print(f"Loaded samples   : {loaded_signal.shape}")
print(f"Data type        : {loaded_signal.dtype}")