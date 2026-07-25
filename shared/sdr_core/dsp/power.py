import numpy as np


def to_db(spectrum: np.ndarray, epsilon: float = 1e-12) -> np.ndarray:
    """
    Convert a linear magnitude spectrum to dB

    Parameters
    ----------
    spectrum : np.ndarray
        FFT amplitude spectrum, linear scale

    epsilon : float
        Small value added before the logarithm to avoid log(0),
        which would create -infinity values

    Returns
    -------
    np.ndarray
        Amplitude spectrum in dB
    """

    return 20 * np.log10(spectrum + epsilon)


def find_peak(freq: np.ndarray, spectrum_db: np.ndarray) -> tuple[float, float]:
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
