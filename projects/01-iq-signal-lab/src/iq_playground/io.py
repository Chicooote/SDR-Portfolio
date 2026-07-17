import numpy as np
from pathlib import Path

def save_iq(iq: np.ndarray, path: Path) -> None:
    """
    Save IQ samples to a NumPy binary (.npy) file

    Parameters
    ----------
    iq : np.ndarray
        Complex IQ samples to save
    path : str
        Path to the output .npy file

    Returns
    -------
    None
    """
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    np.save(path, iq)


def load_iq(path: str) -> np.ndarray:
    """
    Load IQ samples from a NumPy binary (.npy) file

    Parameters
    ----------
    path : str
        Path to the input .npy file

    Returns
    -------
    np.ndarray
        Loaded complex IQ samples
    """
    return np.load(path)