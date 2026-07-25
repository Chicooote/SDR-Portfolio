import numpy as np


def apply_window(iq: np.ndarray) -> np.ndarray:
    """
    Apply a Hann window to a block of IQ samples

    This reduces spectral leakage caused by the DFT's implicit
    assumption that the analyzed block repeats forever: without
    tapering, a non-integer number of cycles in the block creates
    a discontinuity at the wrap-around point, and that discontinuity's
    energy smears into neighboring frequency bins.

    Parameters
    ----------
    iq : np.ndarray
        Complex IQ samples

    Returns
    -------
    np.ndarray
        Windowed IQ samples
    """

    N = len(iq)
    han_window_function = np.hanning(N)

    return iq * han_window_function
