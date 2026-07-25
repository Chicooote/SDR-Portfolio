from iq_playground.signal_generator import generate_complex_tone
from sdr_core.visualization.iq import plot_iq_time, plot_constellation
from sdr_core.visualization.spectrum import plot_spectrum
from sdr_core.dsp.fft import compute_spectrum_db


# Generate a 100 kHz complex sinusoid
# sampled at 1 MHz
fs = 1_000_000
f = 100_000
N = 100

# Application of a Hanning window
window: bool = False

iq = generate_complex_tone(fs, f, N)

plot_iq_time(iq)
plot_constellation(iq)
freq, spectrum_db = compute_spectrum_db(iq, fs, window)
plot_spectrum(freq, spectrum_db)