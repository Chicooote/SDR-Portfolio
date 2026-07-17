# Project 01 — IQ Signal Lab

## 1. Overview

**IQ Signal Lab** is a Python laboratory for generating, manipulating, and analyzing complex IQ (In-phase/Quadrature) signals — the native data format used by Software Defined Radios.

This is the first project in a broader SDR learning path. Before touching real hardware, the goal is to build solid intuition for the math and DSP that every SDR pipeline relies on: complex baseband representation, sampling, and frequency-domain analysis via the FFT. Everything here is built from first principles with NumPy rather than through a high-level DSP framework, so that each transform (windowing, FFT, noise injection) is understood rather than treated as a black box.

**Technologies:** Python, NumPy, Matplotlib.

## 2. Project Scope

This project is deliberately scoped to pure software simulation of the IQ signal model. Hardware acquisition and anything downstream of raw baseband analysis is out of scope here and reserved for later projects (see [Section 14](#14-future-evolution)).

**Included:**
- IQ signal generation (complex exponential from first principles)
- Complex baseband manipulation
- FFT analysis (with and without windowing)
- Noise modeling (AWGN)
- IQ file persistence (`.npy`)

**Not included:**
- RTL-SDR acquisition
- Real-time processing
- Demodulation
- RF protocol decoding

## 3. Technical Objectives

The project demonstrates:

- Generation of complex IQ signals from first principles (Euler's formula)
- Time-domain visualization of the I and Q components
- IQ constellation plotting
- Frequency-domain analysis via FFT, including spectral leakage and Hann windowing
- Simulation of realistic channel impairments (AWGN noise) and their effect on the spectrum and constellation
- Persistence of IQ data to/from disk (`.npy`) for reuse across scripts

Skills targeted: complex-number signal representation, sampling theory, FFT-based spectral analysis, and a package layout that separates signal generation, analysis, visualization, noise modeling, and I/O into independent modules.

## 4. Development Environment

- Windows 11
- Python 3.12
- NumPy
- Matplotlib
- Package managed via `pyproject.toml` (`setuptools`), installed in editable mode

**Hardware validation:** no SDR hardware is used in this project. Planned in a future experiment ([Section 14](#14-future-evolution)):
- RTL-SDR V2
- FC0013 tuner
- Real IQ capture comparison against this simulation

## 5. Project Architecture

```
01-iq-signal-lab/
├── README.md
├── pyproject.toml
├── src/
│   └── iq_playground/
│       ├── signal_generator.py   # Complex tone generation
│       ├── noise.py              # AWGN noise injection
│       ├── analysis.py           # FFT + spectrum plotting
│       ├── visualization.py      # Time-domain + constellation plots
│       └── io.py                 # Save/load IQ samples (.npy)
├── examples/
│   ├── generate_tone.py          # End-to-end: generate → visualize → FFT
│   ├── noise_experiment.py       # Same pipeline with AWGN applied
│   └── save_load_iq.py           # Persist and reload IQ samples
├── data/                         # Saved .npy IQ captures
└── images/                       # Generated plots
```

Each module has a single responsibility, so a full experiment in `examples/` is just a composition of small, independently testable functions.

## 6. How to Run

Install the package in editable mode:

```bash
pip install -e .
```

Run the examples:

```bash
python examples/generate_tone.py
python examples/noise_experiment.py
python examples/save_load_iq.py
```

Each script is self-contained and writes its plots to `images/` and, for `save_load_iq.py`, a sample capture to `data/`.

## 7. Theory

### 7.1 Why Complex (IQ) Representation Exists

A real-valued radio signal only carries amplitude information at each instant — its phase has to be inferred from how the amplitude changes over time, which is ambiguous and noise-sensitive. SDR hardware solves this by mixing the incoming RF signal down to baseband with two mixers driven 90° apart (one by `cos`, one by `sin`), producing two real streams — I and Q — that together encode amplitude **and** phase unambiguously at every sample. Treating the pair `(I, Q)` as one complex number `z = I + jQ` turns every downstream operation (filtering, mixing, demodulation) into ordinary complex arithmetic.

### 7.2 Complex Signals

An IQ sample is a complex number `z = I + jQ`, where `I` is the real part and `Q` is the imaginary part. The same value can be written in polar form:

```
z = A * e^(jθ) = A * (cos θ + j sin θ)
```

where `A = |z|` is the instantaneous amplitude and `θ = atan2(Q, I)` is the instantaneous phase. Representing a radio signal this way lets a single sample carry both pieces of information at once, instead of needing separate magnitude/phase tracking.

### 7.3 IQ Generation from First Principles

A complex sinusoid at frequency `f` is generated directly from Euler's formula:

```python
phase = 2 * np.pi * f * t
iq = np.exp(1j * phase)  # cos(phase) + j*sin(phase)
```

Geometrically, this is a unit vector rotating at rate `f` in the complex plane. The real part (I) and imaginary part (Q) are just its projections onto the horizontal and vertical axes. This representation is what allows SDR hardware to shift a real-world RF signal down to a **complex baseband** signal centered at 0 Hz, keeping both sidebands distinguishable — unlike a real-valued signal, whose spectrum is always mirrored around 0 Hz and cannot distinguish `+f` from `−f`.

### 7.4 Sampling Theory

Two parameters define every signal in this project:

- **Sampling frequency (`fs`)** — how many complex samples are taken per second
- **Number of samples (`N`)** — the length of the capture, which combined with `fs` sets the observation duration (`N / fs`)

The **Nyquist–Shannon sampling theorem** states that a signal can be reconstructed without ambiguity only if it is sampled at more than twice its highest frequency component (`fs > 2 * f_max`). For complex baseband sampling, the usable bandwidth spans the full `[-fs/2, +fs/2]` range (rather than `[0, fs/2]` for real sampling), since I/Q sampling already separates positive and negative frequencies. Sampling below the Nyquist rate causes **aliasing**: a high-frequency component folds back and appears as a false lower-frequency one.

### 7.5 The Discrete Fourier Transform and FFT

The DFT converts a block of `N` time-domain samples into `N` frequency-domain bins:

```
X[k] = Σ(n=0 to N-1) x[n] * e^(-j2πkn/N)
```

The **FFT** (Fast Fourier Transform) computes the exact same result as the DFT in `O(N log N)` instead of `O(N²)`. `analysis.compute_fft` performs three steps:

1. Optionally apply a **Hann window** to taper the edges of the sample block (see [7.6](#76-windowing-and-spectral-leakage))
2. Compute `np.fft.fft` and re-center it with `fftshift` so 0 Hz sits in the middle of the spectrum
3. Build the matching frequency axis with `fftfreq`, and convert the complex spectrum to a normalized magnitude (`|FFT| / N`), later expressed in dB (`20*log10`)

Frequency resolution is `fs / N`: longer captures (more samples) resolve closer tones, at the cost of time resolution — the two are locked in a trade-off for any fixed sampling rate.

### 7.6 Windowing and Spectral Leakage

The DFT implicitly assumes the analyzed block repeats forever (it treats the `N` samples as one period of a periodic signal). If the block doesn't contain an exact integer number of cycles of the tone, there's a discontinuity at the wrap-around point, and that discontinuity's energy smears — **leaks** — into neighboring frequency bins instead of staying in one clean peak.

A **window function** multiplies the sample block by a taper that goes to zero at both edges, removing the discontinuity. The Hann window used here is:

```
w[n] = 0.5 * (1 - cos(2πn / (N-1)))
```

Windowing reduces side-lobe leakage significantly, at the cost of widening the main lobe (lower frequency resolution for closely spaced tones). This main-lobe/side-lobe trade-off is fundamental — no window improves both simultaneously.

### 7.7 Noise Modeling (AWGN)

**AWGN** (Additive White Gaussian Noise) models thermal and receiver noise: uncorrelated, zero-mean Gaussian noise added independently to every sample. For a complex signal, the noise power is split evenly between the I and Q components (`noise_power / 2` each), since total power is the sum of the variances of both parts.

**SNR** (Signal-to-Noise Ratio), expressed in dB, is what actually determines whether a signal is detectable — not its raw amplitude:

```
SNR(dB) = 10 * log10(P_signal / P_noise)
```

Given a target SNR and known signal power, the required noise power is derived and used to scale a complex Gaussian random draw before adding it to the clean signal.

## 8. Software Simulation

This section describes the simulation modules themselves; concrete runs and their results are documented as lab entries in [Section 9 — Experiments](#9-experiments).

### 8.1 Signal Generation

`signal_generator.generate_complex_tone(fs, f, N)` produces a pure complex exponential at a given frequency, per [7.3](#73-iq-generation-from-first-principles):

```python
fs = 1_000_000   # 1 MHz sampling rate
f = 100_000      # 100 kHz tone
N = 100          # number of samples

iq = generate_complex_tone(fs, f, N)
```

### 8.2 Time-Domain Visualization

`visualization.plot_iq_time` plots `iq.real` (I) and `iq.imag` (Q) against the sample index, so the quadrature relationship between the two components can be inspected directly.

### 8.3 IQ Constellation

`visualization.plot_constellation` plots Q against I, giving a geometric view of amplitude and phase per sample rather than a time series.

### 8.4 FFT Spectrum Analysis

`analysis.compute_fft` / the accompanying spectrum plot implement the pipeline described in [7.5](#75-the-discrete-fourier-transform-and-fft), with an optional Hann window applied per [7.6](#76-windowing-and-spectral-leakage).

## 9. Experiments

### Experiment 1 — Pure IQ Tone

**Objective:** verify that a complex exponential generated from first principles produces the expected quadrature relationship between I and Q, and a circular constellation.

**Parameters:** `fs = 1 MHz`, `f = 100 kHz`, `N = 100`.

**Expected result:** I and Q should appear as two sinusoids 90° out of phase (`cos` and `sin` sharing the same instantaneous phase); the constellation should form a clean ring, since every sample has the same amplitude but a different accumulated phase.

**Observed result:**

![IQ signal in time domain](images/iq%20signal%20in%20time%20domain.png)

![IQ constellation](images/iq%20constellation.png)

**Conclusion:** the generated signal matches theory exactly — I/Q are in quadrature and the constellation is a uniform ring, confirming the tone generator is correct before it's used as the basis for the noise and windowing experiments below.

### Experiment 2 — Spectral Leakage

**Objective:** observe spectral leakage from analyzing a finite sample block, and measure how a Hann window mitigates it.

**Parameters:** `fs = 1 MHz`, `f = 100 kHz`, `N = 100` (frequency resolution `fs/N = 10 kHz`).

**Comparison:**

Without window:

![IQ spectrum](images/iq%20spectrum.png)

With Hann window:

![IQ spectrum with Hann window](images/iq%20spectrum%20with%20han%20window.png)

For reference, the constellation is unaffected by windowing (it's a time-domain artifact, not shown in the frequency plot):

![IQ constellation with Hann window](images/iq%20constellation%20with%20han%20window.png)

**Conclusion:** without windowing, energy leaks into neighboring bins because the 100 kHz tone isn't an exact integer number of cycles relative to the DFT's implicit periodicity assumption. The Hann window widens the main lobe slightly but suppresses side-lobe leakage significantly, giving a cleaner, more localized peak — the classic time/frequency resolution trade-off described in [7.6](#76-windowing-and-spectral-leakage).

### Experiment 3 — AWGN Impact

**Objective:** assess how additive Gaussian channel noise degrades the time-domain signal, constellation, and spectrum, and confirm that a peak remains detectable at a realistic SNR.

**Parameters:** `fs = 1 MHz`, `f = 100 kHz`, `N = 1000` (increased from `N = 100` to sharpen frequency resolution and make the noise floor easier to read).

**SNR:** 20 dB.

**Observation:**

![IQ signal noised](images/iq%20signal%20noised.png)

![IQ constellation noised](images/iq%20constellation%20noised.png)

![Spectrum noised](images/spectrum%20noised.png)

**Conclusion:** noise perturbs each sample's magnitude and phase independently, thickening the constellation ring into a fuzzy annulus and adding random fluctuations to both I and Q in the time domain. In the spectrum, the 100 kHz peak is still clearly identifiable above a raised noise floor — illustrating why SNR, not raw amplitude, is the meaningful metric for detectability.

## 10. IQ Data Persistence

`io.save_iq` / `io.load_iq` wrap `numpy.save` / `numpy.load` to persist complex IQ arrays as `.npy` files, creating the destination directory if needed. `examples/save_load_iq.py` verifies round-trip integrity by comparing shape and dtype of the saved and reloaded arrays — this is the same format that would be used to store a real hardware capture, which keeps the simulation and future hardware paths interoperable.

## 11. Results Summary

| Feature | Status |
|---|---|
| IQ generation | ✓ |
| Time visualization | ✓ |
| Constellation analysis | ✓ |
| FFT spectrum | ✓ |
| Hann window | ✓ |
| AWGN simulation | ✓ |
| IQ storage | ✓ |
| RTL-SDR validation | Planned |

## 12. Difficulties Encountered

- Getting the FFT axis conventions right: forgetting `fftshift` on either the spectrum or the frequency axis silently produces a spectrum that's mirrored/misaligned rather than erroring out, which made early plots hard to interpret.
- Building correct complex AWGN: splitting the target noise power evenly between the real and imaginary parts (`noise_power / 2` per component) was necessary to hit the intended SNR — an easy factor to get wrong.
- Understanding *why* windowing trades main-lobe width for side-lobe suppression, rather than just calling `np.hanning` and taking the flatter-looking spectrum on faith.

## 13. Skills Acquired

**Python**
- Structuring a small package with `pyproject.toml` and an editable install
- Writing pure, single-responsibility NumPy functions with clear docstrings

**DSP**
- Complex baseband (IQ) signal representation
- Sampling frequency, sample count, and their relationship to time and frequency resolution
- FFT computation, frequency-axis construction, and spectral leakage
- Window functions (Hann) and the resolution/leakage trade-off
- Modeling AWGN and reasoning about signal-to-noise ratio

**SDR**
- Why SDR systems operate on complex baseband IQ rather than real-valued RF samples
- The link between constellation shape, phase, and noise

**Git/GitHub**
- Incremental, feature-by-feature commit history for a learning project
- Structuring a repository so simulation code, examples, and generated artifacts stay separated

## 14. Future Evolution

This project provides the DSP foundation for future SDR applications:

- Real hardware IQ acquisition
- Signal detection
- Filtering
- Demodulation
- Digital decoding

## 15. Conclusion

This project demonstrates a working, from-scratch understanding of the IQ signal model that underlies all SDR systems: generating complex baseband signals, reasoning about them in both time and frequency domain, and understanding how noise and windowing choices affect what's actually measurable in a spectrum. The FFT pipeline, noise model, and I/O layer built here are intentionally hardware-agnostic, so the same code will apply directly to real RTL-SDR captures.

The next project moves from pure simulation to real hardware acquisition, applying these same analysis tools to signals captured from an RTL-SDR dongle.

The main objective was not only to implement DSP algorithms, but to understand the relationship between mathematical models, software implementation, and real-world measurements.
