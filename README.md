# IQ Playground

A Software Defined Radio (SDR) learning project using Python and RTL-SDR hardware.

## Objectives

This project aims to learn and implement:

- IQ signal processing
- Digital signal processing (DSP)
- FFT and spectrum analysis
- RTL-SDR acquisition
- SDR software architecture
- GNU Radio concepts
- C/C++ SDR development

## Current Features

- Complex IQ tone generation
- IQ constellation visualization
- Time-domain visualization
- FFT spectrum analysis
- Hann window spectral analysis
- RTL-SDR interface architecture

## Technologies

- Python 3.12
- NumPy
- Matplotlib
- pyrtlsdr
- RTL-SDR dongle

## Project Structure


src/

└── iq_playground/

├── signal_generator.py

├── visualization.py

├── analysis.py

└── rtl_device.py


## Roadmap

- [x] Generate IQ signals
- [x] FFT spectrum analyzer
- [x] Spectral leakage study
- [ ] RTL-SDR live acquisition
- [ ] Waterfall display
- [ ] FM demodulator
- [ ] GNU Radio integration
- [ ] C++ SDR processing