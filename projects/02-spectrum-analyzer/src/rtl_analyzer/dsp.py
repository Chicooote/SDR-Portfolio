import numpy as np

def compute_spectrum_db(samples, sample_rate) :
    """
    Compute the magnitude spectrum of complex IQ samples

    Parameters
    ----------
    samples : np.ndarray
        Complex IQ samples

    sample_rate : float
        Sampling frequency in Hz

    Returns
    -------
    freq : np.ndarray
        Frequency axis

    spectrum_db : np.ndarray
        FFT amplitude spectrum in dB
    """

    N = len(samples)
    han_window_function = np.hanning(N)
    samples_processed = samples * han_window_function

    # Transform the IQ samples from time domain to frequency domain
    fft = np.fft.fft(samples_processed)

    # Move the zero frequency component to the center of the spectrum
    fft_shifted = np.fft.fftshift(fft)

    # Create the frequency axis corresponding to the FFT bins
    freq = np.fft.fftshift(
        np.fft.fftfreq(N, 1 / sample_rate)
    )

    # Convert complex FFT values into amplitude spectrum
    spectrum = np.abs(fft_shifted) / N

    # Compute the spectrum in dB
    epsilon = 1e-12
    spectrum_db = 20 * np.log10(spectrum + epsilon)

    return freq, spectrum_db


def find_peak(freq, spectrum_db):
    """
    Find the strongest frequency component in a spectrum

    Parameters
    ----------
    freq : np.ndarray
        Frequency axis, in the same reference (relative or absolute)
        as the one used to compute spectrum_db

    spectrum_db : np.ndarray
        FFT amplitude spectrum in dB

    Returns
    -------
    peak_freq : float
        Frequency of the strongest bin

    peak_amplitude_db : float
        Amplitude of the strongest bin, in dB

    Notes
    -----
    This reports the strongest bin in the spectrum, which may be a carrier,
    an interferer, a local signal, or an artifact - not a signal identification.
    """

    peak_index = np.argmax(spectrum_db)

    return freq[peak_index], spectrum_db[peak_index]
