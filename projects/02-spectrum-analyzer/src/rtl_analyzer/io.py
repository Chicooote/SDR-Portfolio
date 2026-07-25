import json
import numpy as np
from pathlib import Path


def save_iq(iq: np.ndarray, path: Path, metadata: dict) -> None:
    """
    Save real IQ samples to a NumPy binary (.npy) file, alongside a
    JSON sidecar file describing the acquisition parameters

    A raw IQ capture is meaningless without knowing the center
    frequency, sample rate and gain it was acquired with: the same
    bytes could correspond to any signal

    Parameters
    ----------
    iq : np.ndarray
        Complex IQ samples to save

    path : Path
        Path to the output .npy file

    metadata : dict
        Acquisition parameters. Expected keys:
        center_frequency, sample_rate, gain, number_of_samples

    Returns
    -------
    None
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    np.save(path, iq)

    metadata_path = path.with_suffix(".json")
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)


def load_iq(path: Path) -> tuple[np.ndarray, dict]:
    """
    Load real IQ samples and their acquisition metadata

    Parameters
    ----------
    path : Path
        Path to the input .npy file

    Returns
    -------
    iq : np.ndarray
        Loaded complex IQ samples

    metadata : dict
        Acquisition parameters saved alongside the samples
        (center_frequency, sample_rate, gain, number_of_samples)
    """
    path = Path(path)
    iq = np.load(path)

    metadata_path = path.with_suffix(".json")
    with open(metadata_path) as f:
        metadata = json.load(f)

    return iq, metadata
