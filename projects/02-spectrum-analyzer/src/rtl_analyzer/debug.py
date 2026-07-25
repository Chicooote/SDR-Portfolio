import numpy as np


def print_acquisition_info(dongle, samples) -> None:
    """
    Print raw acquisition statistics for a debugging session

    Parameters
    ----------
    dongle : RTLDevice
        The device the samples were acquired from, used to report
        the acquisition parameters alongside the sample statistics

    samples : np.ndarray
        Complex IQ samples acquired from the dongle
    """

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
