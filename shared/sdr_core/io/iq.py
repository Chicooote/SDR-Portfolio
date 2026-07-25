import json
import numpy as np
from pathlib import Path


def save_iq(iq: np.ndarray, path: Path, metadata: dict | None = None) -> None:
    """
    Save IQ samples to a NumPy binary (.npy) file, optionally alongside a
    JSON sidecar file describing the acquisition parameters

    A raw IQ capture is meaningless without knowing the center
    frequency, sample rate and gain it was acquired with: the same
    bytes could correspond to any signal. For purely simulated signals
    this metadata may be omitted.

    Parameters
    ----------
    iq : np.ndarray
        Complex IQ samples to save

    path : Path
        Path to the output .npy file

    metadata : dict, optional
        Acquisition parameters (e.g. center_frequency, sample_rate,
        gain, number_of_samples). When provided, saved as a JSON
        sidecar next to the .npy file.

    Returns
    -------
    None
    """

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    np.save(path, iq)

    if metadata is not None:
        metadata_path = path.with_suffix(".json")
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)


def load_iq(path: Path) -> tuple[np.ndarray, dict | None]:
    """
    Load IQ samples and their acquisition metadata, if any

    Parameters
    ----------
    path : Path
        Path to the input .npy file

    Returns
    -------
    iq : np.ndarray
        Loaded complex IQ samples

    metadata : dict or None
        Acquisition parameters saved alongside the samples, or None
        if no JSON sidecar file exists
    """

    path = Path(path)
    iq = np.load(path)

    metadata_path = path.with_suffix(".json")
    metadata = None
    if metadata_path.exists():
        with open(metadata_path) as f:
            metadata = json.load(f)

    return iq, metadata
