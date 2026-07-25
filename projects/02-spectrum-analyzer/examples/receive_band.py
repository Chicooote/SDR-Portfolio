from sdr_core.io.rtl_sdr import RTLDevice
from sdr_core.dsp.fft import compute_spectrum_db
from sdr_core.dsp.power import find_peak
from sdr_core.visualization.iq import plot_iq_time, plot_constellation
from sdr_core.visualization.spectrum import plot_spectrum

dongle = RTLDevice()

dongle.open()

dongle.configure(100_000_000, 2_400_000, 20)

samples = dongle.read_samples(10000)
sample_rate = dongle.sample_rate
plot_iq_time(samples)
plot_constellation(samples)

freq_relative, spectrum_db = compute_spectrum_db(samples, sample_rate)

# sdr_core.dsp stays generic and only knows about frequencies relative to
# baseband (0 Hz = center_frequency); the absolute RF frequency is
# reconstructed here, at the orchestration level.
freq_absolute = freq_relative + dongle.center_frequency

peak_freq_relative, peak_amplitude_db = find_peak(freq_relative, spectrum_db)
peak_freq_absolute = peak_freq_relative + dongle.center_frequency

print(f"Peak relative frequency : {peak_freq_relative / 1e3:+.1f} kHz")
print(f"Peak RF frequency       : {peak_freq_absolute / 1e6:.3f} MHz")
print(f"Peak amplitude          : {peak_amplitude_db:.1f} dB")

plot_spectrum(freq_absolute / 1e6, spectrum_db, peak_freq_absolute / 1e6, peak_amplitude_db, freq_unit="MHz")


dongle.close()