import numpy as np
import matplotlib.pyplot as plt

def print_acquisition_info(dongle, samples):

    print(type(samples))
    print(samples.shape)
    print(samples.dtype)
    print(samples[:5])

    print(f" min I : {min(samples.real)}")
    print(f" max I : {max(samples.real)}")
    print(f" mean I : {np.mean(samples.real)}")
    print(f" std I : {np.std(samples.real)}")

    print(f" min Q : {min(samples.imag)}")
    print(f" max Q : {max(samples.imag)}")
    print(f" mean Q : {np.mean(samples.imag)}")
    print(f" std Q : {np.std(samples.imag)}")

    print(f"center frequency :{dongle.center_frequency} Hz")
    print(f"sample rate : {dongle.sample_rate} Hz")
    print(f"gain : {dongle.gain} dB")

def plot_iq_time(iq : np.ndarray)-> None:
    """
    Display the in-phase (I) and quadrature (Q) components
    of a complex IQ signal in the time domain

    Parameters
    ----------
    iq : np.ndarray
        Complex IQ samples
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
    Display the IQ constellation

    The x-axis represents the in-phase component (I)
    and the y-axis represents the quadrature component (Q)

    Parameters
    ----------
    iq : np.ndarray
        Complex IQ samples
    """

    plt.scatter(iq.real, iq.imag, s=10)

    plt.xlabel("I")
    plt.ylabel("Q")
    plt.title("IQ constellation")

    plt.axis("equal")
    plt.grid()
    plt.show()

def plot_spectrum(
    freq: np.ndarray,
    spectrum_db: np.ndarray,
    peak_freq: float | None = None,
    peak_amplitude_db: float | None = None,
) -> None:
    """
    Display the frequency spectrum in dB

    Parameters
    ----------
    freq : np.ndarray
        Frequency axis in Hz (relative or absolute RF frequency)

    spectrum_db : np.ndarray
        FFT amplitude spectrum in dB

    peak_freq : float, optional
        Frequency of a peak to highlight on the plot, in Hz

    peak_amplitude_db : float, optional
        Amplitude of the peak to highlight, in dB
    """

    freq_mhz = freq / 1e6

    plt.plot(freq_mhz, spectrum_db)

    if peak_freq is not None and peak_amplitude_db is not None:
        plt.scatter(
            [peak_freq / 1e6],
            [peak_amplitude_db],
            color="red",
            zorder=5,
            label=f"Peak: {peak_freq / 1e6:.3f} MHz",
        )
        plt.legend()

    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Amplitude (dB)")
    plt.title("IQ Spectrum")

    plt.grid()
    plt.show()