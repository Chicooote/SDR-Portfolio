import matplotlib.pyplot as plt

from iq_playground.signal_generator import generate_complex_tone

fs = 1000000
f = 100000
N = 1000
cmpl_tone = generate_complex_tone(fs, f, N)

plt.plot(cmpl_tone.real, label="I")
plt.plot(cmpl_tone.imag, label="Q")

plt.legend()
plt.grid()
plt.show()