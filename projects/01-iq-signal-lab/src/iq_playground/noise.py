import numpy as np


def add_awgn_noise(iq: np.ndarray, snr_db: float, enable_noise: bool=True) -> np.ndarray:
    """
    Add complex Additive White Gaussian Noise (AWGN) to IQ samples

    Parameters
    ----------
    iq : np.ndarray
        Complex IQ samples

    snr_db : float
        Desired signal-to-noise ratio in decibels
        Higher values produce a cleaner signal

    noise : bool
        Apply noise to the IQ sample

    Returns
    -------
    np.ndarray
        IQ samples with added complex Gaussian noise
    """

    if enable_noise:
        # Estimate the average signal power from the complex IQ samples
        # Power is calculated from the magnitude because IQ samples contain
        # both real (I) and imaginary (Q) components.
        signal_power = np.mean(np.abs(iq) ** 2)

        # Convert SNR from decibels to a linear power ratio
        # The noise power calculation must use the linear value, not dB
        snr_linear = 10 ** (snr_db / 10)

        # Calculate the noise power required to reach the target SNR
        noise_power = signal_power / snr_linear

        # Generate complex Gaussian noise
        # The factor of 1/2 distributes the noise power equally between
        # the real (I) and imaginary (Q) components
        noise = (
            np.random.normal(
                0,
                np.sqrt(noise_power / 2),
                iq.shape
            )
            +
            1j * np.random.normal(
                0,
                np.sqrt(noise_power / 2),
                iq.shape
            )
        )

        # Add the generated noise to the original IQ signal
        # The result simulates a more realistic SDR acquisition
        iq_noisy = iq + noise
    else:
        iq_noisy = iq

    return iq_noisy