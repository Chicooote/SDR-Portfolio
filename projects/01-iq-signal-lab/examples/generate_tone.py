from iq_playground.signal_generator import generate_complex_tone
from iq_playground.visualization import plot_iq_time, plot_constellation
from iq_playground.analysis import compute_fft, plot_spectrum
from iq_playground.noise import add_awgn_noise


# Generate a 100 kHz complex sinusoid
# sampled at 1 MHz
fs = 1_000_000
f = 100_000
N = 1000
# Signal-to-noise ratio
snr_db = 20

# Application of a Hanning window
window: bool = True
enable_noise: bool = False

iq = generate_complex_tone(fs, f, N)
iq = add_awgn_noise(iq, snr_db=snr_db, enable_noise=enable_noise)

plot_iq_time(iq)
plot_constellation(iq)
freq, spectrum = compute_fft(iq,fs, window)
plot_spectrum(freq, spectrum)