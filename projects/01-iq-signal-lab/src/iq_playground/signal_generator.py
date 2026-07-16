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
    
    # Create an array of sample indices from 0 to N-1
    n = np.arange(N)

    # Convert sample indices into time values using the sampling frequency
    # t represents the time instant of each sample
    t = n / fs

    # Compute the instantaneous phase of the complex sinusoid
    # The phase evolves according to: phase = 2*pi*f*t
    phase = 2 * np.pi * f * t

    # Generate the complex exponential signal using Euler's formula:
    # exp(j*phase) = cos(phase) + j*sin(phase)
    # The real part represents the I (In-phase) component
    # The imaginary part represents the Q (Quadrature) component
    iq = np.exp(1j * phase)

    # Return the generated complex IQ samples
    return iq