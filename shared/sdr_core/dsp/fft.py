import numpy as np

from sdr_core.dsp.windows import apply_window
from sdr_core.dsp.power import to_db


def compute_fft(iq: np.ndarray, fs: float, window: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the FFT magnitude spectrum of complex IQ samples

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
        FFT amplitude spectrum, linear scale
    """

    N = len(iq)
    iq_processed = apply_window(iq) if window else iq

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


def compute_spectrum_db(iq: np.ndarray, fs: float, window: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """
    Compute the FFT magnitude spectrum of complex IQ samples, in dB

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

    spectrum_db : np.ndarray
        FFT amplitude spectrum in dB
    """

    freq, spectrum = compute_fft(iq, fs, window)

    return freq, to_db(spectrum)
