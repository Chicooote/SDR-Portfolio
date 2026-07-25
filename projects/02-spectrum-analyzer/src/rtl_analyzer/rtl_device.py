from rtlsdr import RtlSdr
import numpy as np

class RTLDevice:
    """
    Interface used to control an RTL-SDR receiver

    This class is responsible for configuring the SDR,
    reading IQ samples and managing the connection with
    the hardware
    """

    def __init__(self) -> None:
        """
        Initialize the RTL-SDR device state
        """

        # Hardware interface (created when the device is opened)
        # This is the single source of truth for the connection state:
        # there is no separate "connected" flag to keep in sync
        self.sdr: RtlSdr | None = None

        # SDR parameters
        self.center_frequency: float | None = None
        self.sample_rate: float | None = None
        self.gain: float | None = None

    @property
    def is_connected(self) -> bool:
        """
        Whether the RTL-SDR dongle is currently open
        """

        return self.sdr is not None


    def open(self) -> None:
        """
        Open communication with the RTL-SDR dongle
        """

        self.sdr = RtlSdr()


    def close(self) -> None:
        """
        Close communication with the RTL-SDR dongle
        """

        if self.sdr is not None:
            self.sdr.close()

        self.sdr = None

    def configure(
        self,
        center_frequency: float,
        sample_rate: float,
        gain: float,
    ) -> None:
        """
        Configure SDR parameters

        Parameters
        ----------
        center_frequency : float
            Receiver center frequency in Hz

        sample_rate : float
            ADC sampling frequency in samples per second

        gain : float
            Receiver gain in dB
        """

        if self.sdr is None:
            raise RuntimeError("RTL-SDR device is not open")

        self.center_frequency = center_frequency
        self.sample_rate = sample_rate
        self.gain = gain

        self.sdr.center_freq = center_frequency
        self.sdr.sample_rate = sample_rate
        self.sdr.gain = gain


    def read_samples(self, number_of_samples: int) -> np.ndarray:
        """
        Read IQ samples from the RTL-SDR

        Parameters
        ----------
        number_of_samples : int
            Number of complex IQ samples to acquire

        Returns
        -------
        np.ndarray
            Complex IQ samples
        """

        if self.sdr is None:
            raise RuntimeError("RTL-SDR device is not open")

        iq_samples = self.sdr.read_samples(number_of_samples)

        return np.asarray(iq_samples, dtype=np.complex64)