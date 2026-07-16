import numpy as np
import matplotlib.pyplot as plt

def compute_fft(iq: np.ndarray, fs: float, window: bool=True): 
    """
    Compute the FFT of IQ samples

    Parameters
    ----------
    iq : np.ndarray
        Complex IQ samples

    fs : float
        Sampling frequency in Hz

    window : bool
        Apply a Hann window before FFT to reduce spectral leakage

    Returns
    -------
    freq : np.ndarray
        Frequency axis

    spectrum : np.ndarray
        FFT amplitude spectrum
    """
    N = len(iq)

    # Apply a Hann window before FFT
    # This reduces spectral leakage caused by cutting the signal abruptly
    if window:
        han_window_function = np.hanning(N)
        iq_processed = iq * han_window_function
    else:
        iq_processed = iq

    # Transform the IQ samples from time domain to frequency domain
    fft = np.fft.fft(iq_processed)

    # Move the zero frequency component to the center of the spectrum
    fft_shifted = np.fft.fftshift(fft)

    # Create the frequency axis corresponding to the FFT bins
    freq = np.fft.fftshift(
        np.fft.fftfreq(N, 1 / fs)
    )

    # Convert complex FFT values into amplitude spectrum
    spectrum = np.abs(fft_shifted) / N

    return freq, spectrum


def plot_spectrum(freq: np.ndarray, spectrum: np.ndarray):
    """
    Display the frequency spectrum in dB

    Parameters
    ----------
    freq : np.ndarray
        Frequency axis in Hz

    spectrum : np.ndarray
        FFT amplitude spectrum
    """

    # Avoid log(0), which would create -infinity values
    epsilon = 1e-12

    spectrum_db = 20 * np.log10(spectrum + epsilon)

    plt.plot(freq, spectrum_db)

    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (dB)")
    plt.title("IQ Spectrum")

    plt.grid()
    plt.show()