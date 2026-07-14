import numpy as np

def generate_complex_tone(fs: float, f: float, N: int,) -> np.ndarray:
    """
    Generate a complex exponential

    Parameters
    ----------
    fs : float
        Sampling frequency in Hz

    f : float
        Signal frequency in Hz

    N : int
        Number of samples

    Returns
    -------
    np.ndarray
        Complex IQ samples
    """
    
    n = np.arange(N)

    t = n/fs        #temps

    phase = 2*np.pi*f*t

    iq = np.exp(1j * phase)

    return iq
