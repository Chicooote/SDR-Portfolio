from rtl_analyzer.rtl_device import RTLDevice
from rtl_analyzer.io import save_iq, load_iq

dongle = RTLDevice()

dongle.open()

dongle.configure(100_000_000, 2_400_000, 20)

number_of_samples = 10000
samples = dongle.read_samples(number_of_samples)

dongle.close()

metadata = {
    "center_frequency": dongle.center_frequency,
    "sample_rate": dongle.sample_rate,
    "gain": dongle.gain,
    "number_of_samples": number_of_samples,
}

file_path = "02-spectrum-analyzer/data/capture.npy"

# Save the real IQ capture along with its acquisition metadata
save_iq(samples, file_path, metadata)

# Load it back
loaded_samples, loaded_metadata = load_iq(file_path)

print(f"Original samples : {samples.shape}")
print(f"Loaded samples   : {loaded_samples.shape}")
print(f"Data type        : {loaded_samples.dtype}")
print(f"Metadata         : {loaded_metadata}")
