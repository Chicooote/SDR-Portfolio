import matplotlib.pyplot as plt
import numpy as np 

def plot_iq_time(iq : np.ndarray)-> None:
    """
    Display the in-phase (I) and quadrature (Q) components
    of a complex IQ signal in the time domain.

    Parameters
    ----------
    iq : np.ndarray
        Complex IQ samples.
    """

    samples = np.arange(len(iq))
    
    # The real part represents the in-phase component (I)
    # The imaginary part represents the quadrature component (Q)
    plt.plot(samples, iq.real, label="I")
    plt.plot(samples, iq.imag, label="Q")

    plt.xlabel("Sample index")
    plt.ylabel("Amplitude")
    plt.title("IQ signal in time domain")

    plt.legend()
    plt.grid()
    plt.show()


def plot_constellation(iq : np.ndarray)-> None:
    """
    Display the IQ constellation.

    The x-axis represents the in-phase component (I),
    and the y-axis represents the quadrature component (Q).

    Parameters
    ----------
    iq : np.ndarray
        Complex IQ samples.
    """

    plt.scatter(iq.real, iq.imag, s=10)

    plt.xlabel("I")
    plt.ylabel("Q")
    plt.title("IQ constellation")

    plt.axis("equal")
    plt.grid()
    plt.show()