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
└── projects/
    ├── 01-iq-signal-lab/
    └── 02-spectrum-analyzer/
```

Each project is self-contained with its own `README.md`, `src/`, `examples/`, and `pyproject.toml`.
