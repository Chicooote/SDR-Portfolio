# Project 02 — Spectrum Analyzer

## 1. Overview

**Spectrum Analyzer** moves the DSP pipeline built in [Project 01 — IQ Signal Lab](../01-iq-signal-lab) from pure simulation to real hardware: an RTL-SDR dongle now supplies the IQ samples, and the same FFT/spectrum tooling is applied to signals actually pulled from the air instead of a synthetic complex exponential.

The goal here is not to build a full-featured spectrum analyzer application, but to validate that the theory from Project 01 (complex baseband, FFT, windowing) survives contact with real, noisy, quantized hardware data — and to build the acquisition/persistence layer that every later SDR project (filtering, demodulation, decoding) will depend on.

**Technologies:** Python, NumPy, Matplotlib, `pyrtlsdr` (RTL-SDR driver bindings).

## 2. Project Scope

This project covers real IQ acquisition from an RTL-SDR dongle, peak detection on the resulting spectrum, and persistence of a capture alongside its acquisition parameters. Demodulation and protocol-level decoding remain out of scope (see [Section 14](#14-future-evolution)).

**Included:**
- RTL-SDR device control (open/configure/close)
- Real IQ acquisition over USB
- FFT spectrum analysis reusing the windowing approach from Project 01
- Peak detection, with conversion from baseband-relative to absolute RF frequency
- IQ capture persistence (`.npy` + JSON metadata sidecar)

**Not included:**
- Demodulation (AM/FM/etc.)
- RF protocol decoding
- Real-time / streaming acquisition (captures are single fixed-length blocks)
- Multi-channel or wideband scanning

## 3. Technical Objectives

The project demonstrates:

- Driving an RTL-SDR dongle end-to-end: opening the device, configuring center frequency / sample rate / gain, and reading a block of complex IQ samples
- Reusing the Project 01 FFT/windowing pipeline unchanged on real acquisition data
- Distinguishing baseband-relative frequency (what the FFT actually produces, centered on 0 Hz) from absolute RF frequency (relative frequency + center frequency), and keeping that conversion at the orchestration layer rather than inside the DSP module
- Automated peak detection on a real, noisy spectrum
- Persisting a raw IQ capture together with the acquisition parameters needed to make sense of it later

Skills targeted: hardware I/O via a Python driver binding, keeping DSP code hardware-agnostic (generic relative-frequency in, absolute-frequency conversion out), and recognizing real-world ADC artifacts (quantization, settling time) that never show up in a pure simulation.

## 4. Development Environment

- Windows 11
- Python 3.12
- NumPy, Matplotlib
- `pyrtlsdr` (Python bindings over `librtlsdr`)
- Package managed via `pyproject.toml` (`setuptools`), installed in editable mode

**Hardware:**
- RTL-SDR V2 dongle
- FC0013 tuner chip
- 8-bit ADC (a source of the quantization effects discussed in [Section 9](#9-experiments))

This is the hardware validation planned at the end of Project 01: the same complex-baseband model is now exercised against a real receiver instead of `np.exp`.

## 5. Project Architecture

```
02-spectrum-analyzer/
├── README.md
├── pyproject.toml
├── src/
│   └── rtl_analyzer/
│       └── debug.py              # print_acquisition_info: raw sample/parameter dump
├── examples/
│   ├── receive_band.py           # End-to-end: acquire → visualize → FFT → peak
│   └── save_iq_capture.py        # Acquire, persist, and reload a capture
├── data/                         # Saved .npy captures + .json metadata sidecars
└── images/                       # Generated plots
```

The RTL-SDR device wrapper, FFT/peak-detection pipeline, plotting, and IQ+metadata persistence all live in the shared [`sdr_core`](../../shared/sdr_core) package (`sdr_core.io.rtl_sdr`, `sdr_core.dsp`, `sdr_core.visualization`, `sdr_core.io.iq`) — the same code used by Project 01, now exercised against real hardware. `rtl_analyzer` itself only keeps `debug.py`, a small acquisition-debugging helper that isn't reused elsewhere.

## 6. How to Run

Install the shared package, then this one, in editable mode:

```bash
pip install -e ../../shared
pip install -e .
```

With an RTL-SDR dongle connected:

```bash
python examples/receive_band.py
python examples/save_iq_capture.py
```

`receive_band.py` acquires a block of IQ samples, plots the time-domain signal, constellation and spectrum, and prints the strongest detected peak (relative and absolute RF frequency). `save_iq_capture.py` acquires a capture and round-trips it through `sdr_core.io.iq.save_iq` / `load_iq`.

## 7. Theory

### 7.1 From Simulated to Real IQ

Project 01 generated IQ samples directly from Euler's formula. A real RTL-SDR dongle produces the same `I + jQ` representation in hardware: the FC0013 tuner mixes the incoming RF down to a low intermediate frequency, and the ADC digitizes it into the complex baseband stream `pyrtlsdr` hands back as `read_samples()`. The DSP built in Project 01 (FFT, windowing, magnitude spectrum) needs no changes to operate on this data — the whole point of the complex-baseband model is that it doesn't care whether the samples came from a formula or an antenna.

### 7.2 Relative vs. Absolute Frequency

The FFT only ever sees the signal *after* it has been mixed down to baseband, so `sdr_core.dsp.fft.compute_spectrum_db` naturally produces a frequency axis centered on 0 Hz — a **relative** frequency, offset from whatever the tuner was told to center on. The **absolute** RF frequency a bin corresponds to is recovered with a single addition:

```python
freq_absolute = freq_relative + dongle.center_frequency
```

This conversion is deliberately kept in `examples/receive_band.py` rather than inside `sdr_core.dsp`: the DSP module stays generic and hardware-agnostic (it would work identically on a simulated signal), while the orchestration script is the only place that knows about the specific hardware configuration in use.

### 7.3 Peak Detection

`sdr_core.dsp.power.find_peak` reports the strongest bin in a spectrum (`argmax` over `spectrum_db`). On a real, populated RF band this is not a signal *identification* — it's simply the loudest thing present, which could be a genuine broadcast carrier, an interferer, or a hardware artifact. Distinguishing those requires the demodulation and protocol context planned for later projects ([Section 14](#14-future-evolution)).

### 7.4 Quantization and ADC Artifacts

Unlike the noiseless-until-told-otherwise simulation in Project 01, a real 8-bit ADC only offers a finite set of output levels. This is visible directly in [Experiment 1](#experiment-1--acquiring-a-real-fm-broadcast-block): the constellation forms a discrete lattice of points rather than a smooth cloud, and the time-domain I/Q traces show visible plateaus — these are quantization steps, not noise in the AWGN sense from Project 01.

## 8. Software Implementation

This section describes the modules themselves; a concrete run and its results are documented in [Section 9 — Experiments](#9-experiments).

### 8.1 Hardware Interface

`RTLDevice` (`sdr_core.io.rtl_sdr`) wraps `pyrtlsdr.RtlSdr` and tracks connection state through the presence of the underlying `sdr` handle itself (`is_connected`), rather than a separate boolean that could drift out of sync:

```python
dongle = RTLDevice()
dongle.open()
dongle.configure(center_frequency=100_000_000, sample_rate=2_400_000, gain=20)
samples = dongle.read_samples(10_000)
dongle.close()
```

### 8.2 Spectrum Analysis

`sdr_core.dsp.fft.compute_spectrum_db` applies the same Hann-windowed FFT pipeline from Project 01 ([Section 7.5–7.6 there](../01-iq-signal-lab/README.md#75-the-discrete-fourier-transform-and-fft)) to real samples, returning a relative frequency axis and the magnitude spectrum in dB. `sdr_core.dsp.power.find_peak` then scans that spectrum for its strongest bin.

### 8.3 Visualization

`sdr_core.visualization` provides the same time-domain and constellation plots as Project 01, plus `spectrum.plot_spectrum`, which can highlight a detected peak with its frequency and amplitude annotated on the plot; this example converts the frequency axis to MHz before plotting.

## 9. Experiments

### Experiment 1 — Acquiring a Real FM Broadcast Block

**Objective:** acquire a real IQ block centered in the FM broadcast band and verify the full pipeline (acquisition → time domain → constellation → FFT → peak detection) against actual, noisy, quantized hardware data.

**Parameters:** `center_frequency = 100 MHz`, `sample_rate = 2.4 MHz`, `gain = 20 dB`, `N = 10,000` samples.

**Observed result:**

![IQ signal in time domain](images/IQ%20signal%20in%20time%20domain.png)

![IQ constellation](images/IQ%20constellation.png)

![IQ spectrum](images/IQ%20spectrum.png)

**Conclusion:** the spectrum shows two clear peaks, each roughly 200 kHz wide — consistent with FM broadcast channels — with the strongest one detected at **100.691 MHz**, above a noise floor around −90 dB. Unlike Project 01's smooth simulated constellation, this one forms a visible discrete lattice: the RTL-SDR's 8-bit ADC only has a finite number of output levels, so real captures are quantized in a way pure simulation never shows. The first ~2,000 samples in the time-domain plot also sit near zero before the signal reaches its steady-state amplitude — a settling artifact from the tuner/AGC immediately after `configure()`, worth discarding in later projects rather than treating as signal.

## 10. IQ Data Persistence

`sdr_core.io.iq.save_iq` / `load_iq` extend Project 01's `.npy` persistence with an optional JSON metadata sidecar (`center_frequency`, `sample_rate`, `gain`, `number_of_samples`) saved next to each capture whenever a `metadata` dict is passed in. A raw IQ file is just a block of complex numbers — without the acquisition parameters it was captured under, the same bytes could correspond to any signal, so the sidecar is not optional bookkeeping but part of what makes a capture reproducible and reusable later.

## 11. Results Summary

| Feature | Status |
|---|---|
| RTL-SDR device control | ✓ |
| Real IQ acquisition | ✓ |
| FFT spectrum (reused from Project 01) | ✓ |
| Relative → absolute frequency conversion | ✓ |
| Peak detection | ✓ |
| IQ + metadata persistence | ✓ |
| Demodulation | Planned |

## 12. Difficulties Encountered

- Keeping `sdr_core.dsp` hardware-agnostic: it would have been easy to bake `center_frequency` into the spectrum computation, but that would tie generic DSP code to a specific acquisition. Moving the relative-to-absolute conversion into the orchestration script instead kept the module reusable for simulated signals too.
- Recognizing quantization artifacts as real hardware behavior rather than a bug: the lattice-shaped constellation and stepped time-domain plateaus looked wrong at first, until traced back to the ADC's finite resolution.
- A raw `.npy` capture is meaningless on its own — losing track of the center frequency or sample rate it was acquired under makes the file useless, which is what motivated the optional JSON metadata sidecar in `sdr_core.io.iq`.

## 13. Skills Acquired

**Python**
- Wrapping a hardware driver (`pyrtlsdr`) behind a small, single-responsibility class
- Using a resource handle itself as the source of truth for connection state instead of a redundant flag

**DSP**
- Applying an FFT/windowing pipeline validated on simulated data directly to real acquisition data, unchanged
- Distinguishing relative (baseband) frequency from absolute RF frequency, and where that conversion belongs architecturally
- Peak detection on a real, noisy spectrum

**SDR**
- RTL-SDR hardware architecture (FC0013 tuner + ADC) and its role in producing a complex baseband stream
- Recognizing real-world ADC artifacts (quantization, tuner settling time) that don't appear in pure simulation

**Git/GitHub**
- Extending a previous project's module layout (`iq_playground` → `rtl_analyzer`) instead of starting from scratch, so the DSP core stayed proven and stable

## 14. Future Evolution

This project provides the real-hardware acquisition layer for future SDR applications:

- Demodulation (starting with FM broadcast, given the signals already visible in [Experiment 1](#experiment-1--acquiring-a-real-fm-broadcast-block))
- Filtering (channel selection around a detected peak)
- Continuous / streaming acquisition instead of fixed-length blocks
- RF protocol decoding

## 15. Conclusion

This project confirms that the complex-baseband model, FFT pipeline, and persistence layer built in Project 01 transfer directly to real hardware: the same `dsp.py`-style windowed FFT that analyzed a synthetic tone now detects real FM broadcast carriers pulled from an RTL-SDR dongle, with only a thin acquisition and frequency-conversion layer added on top. It also surfaced the first genuinely hardware-specific concerns — ADC quantization and tuner settling time — that a pure simulation could never have revealed.

The next step is to start acting on what's now being detected: demodulating a selected peak instead of only locating it.
