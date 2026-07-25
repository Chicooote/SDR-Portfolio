# SDR Portfolio

A collection of Software Defined Radio (SDR) learning projects using Python, exploring IQ signal processing, DSP, and RTL-SDR hardware.

## Projects

| Project | Description |
| --- | --- |
| [01-iq-signal-lab](projects/01-iq-signal-lab) | Simulated IQ tone generation, FFT/spectrum analysis, windowing, and AWGN noise modeling from first principles. |
| [02-spectrum-analyzer](projects/02-spectrum-analyzer) | Real IQ acquisition from an RTL-SDR dongle, applying the Project 01 FFT pipeline to detect peaks in a live RF band. |

## Structure

```
sdr-portfolio/
├── README.md
├── shared/
│   └── sdr_core/          # DSP, I/O and visualization code shared across projects
└── projects/
    ├── 01-iq-signal-lab/
    └── 02-spectrum-analyzer/
```

`shared/sdr_core` holds the FFT/windowing pipeline, IQ persistence, RTL-SDR device wrapper, and plotting helpers that are common to every project, so each project only implements what's actually specific to it. Each project is self-contained with its own `README.md`, `src/`, `examples/`, and `pyproject.toml`, and depends on `sdr_core` as an editable local package.

## Setup

Install the shared package first, then each project you want to run:

```bash
pip install -e ./shared
pip install -e ./projects/01-iq-signal-lab
pip install -e ./projects/02-spectrum-analyzer
```
