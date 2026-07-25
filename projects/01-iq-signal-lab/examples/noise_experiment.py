from iq_playground.signal_generator import generate_complex_tone
from iq_playground.noise import add_awgn_noise
from sdr_core.visualization.iq import plot_iq_time, plot_constellation
from sdr_core.visualization.spectrum import plot_spectrum
from sdr_core.dsp.fft import compute_spectrum_db

# Generate a 100 kHz complex sinusoid
# sampled at 1 MHz
fs = 1_000_000
f = 100_000
N = 1000
# Signal-to-noise ratio
snr_db = 20

# Application of a Hanning window
window: bool = False
enable_noise: bool = True

iq = generate_complex_tone(fs, f, N)
iq_noisy = add_awgn_noise(iq, snr_db=snr_db, enable_noise=enable_noise)

plot_iq_time(iq_noisy)
plot_constellation(iq_noisy)
freq, spectrum_db = compute_spectrum_db(iq_noisy, fs, window)
plot_spectrum(freq, spectrum_db)