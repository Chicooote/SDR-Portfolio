import numpy as np
import matplotlib.pyplot as plt


def plot_spectrum(
    freq: np.ndarray,
    spectrum_db: np.ndarray,
    peak_freq: float | None = None,
    peak_amplitude_db: float | None = None,
    freq_unit: str = "Hz",
) -> None:
    """
    Display the frequency spectrum in dB

    Parameters
    ----------
    freq : np.ndarray
        Frequency axis, already expressed in `freq_unit`

    spectrum_db : np.ndarray
        FFT amplitude spectrum in dB

    peak_freq : float, optional
        Frequency of a peak to highlight on the plot, in `freq_unit`

    peak_amplitude_db : float, optional
        Amplitude of the peak to highlight, in dB

    freq_unit : str
        Unit of the frequency axis, used for the x-axis label only
        (e.g. "Hz", "kHz", "MHz")
    """

    plt.plot(freq, spectrum_db)

    if peak_freq is not None and peak_amplitude_db is not None:
        plt.scatter(
            [peak_freq],
            [peak_amplitude_db],
            color="red",
            zorder=5,
            label=f"Peak: {peak_freq:.3f} {freq_unit}",
        )
        plt.legend()

    plt.xlabel(f"Frequency ({freq_unit})")
    plt.ylabel("Amplitude (dB)")
    plt.title("IQ Spectrum")

    plt.grid()
    plt.show()
