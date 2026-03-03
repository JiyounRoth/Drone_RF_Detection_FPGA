import numpy as np
import matplotlib.pyplot as plt

from signal_gen import IQSignalGenerator
from plot_utils import PlotUtils

# =======================================
# Parameters
# =======================================
fs = 100000000      # 100 MSPS
duration = 0.01     # 10 ms signal duration
IF_freq = 70000000  # 70 MHz intermediate frequency
Alias_freq = 30000000  # 30 MHz alias frequency
FFT_size = 2048     
slide_size = 512    # 75% overlap
SNR_dB = 10         # Desired SNR in dB
# Complex Drone Signal
engine_rpm = 6000   # RPM of drone motors
blades = 2         # Number of blades per motor
mod_index = 0.5    # Modulation index for AM modulation
hopping_freqs = [65e6, 75e6, 68e6, 72e6]  # Frequencies for frequency hopping (30 MHz to 45 MHz)
hop_duration = 5e-6 # Duration of each hop in seconds
beta = 0.01          # Modulation index for FM modulation
video_bw_mhz=5.0 
deviation_mhz=8.0

# =======================================
# 1. Generate aliased IQ signal
# =======================================
iq_gen = IQSignalGenerator(fs, duration)
t, iq_signal = iq_gen.generate_tone(IF_freq)

# plot in time and frequency domain
PlotUtils.plot_time_freq(t, fs, iq_signal, FFT_size,"Original IQ")

# ==============================================
# 2. Add Gaussian noise to achieve SNR of 10 dB
#    SNR (dB) = 10 * log10(P_signal / P_noise)
# ==============================================
noisy_drone_signal = iq_gen.add_white_noise(iq_signal, SNR_dB)
# plot in time and frequency domain
PlotUtils.plot_time_freq(t, fs, noisy_drone_signal, FFT_size,"Noisy IQ")

# apply hanning window to reduce spectral leakage
windowed_signal = iq_gen.apply_hanning_window(noisy_drone_signal)
# plot in time and frequency domain
PlotUtils.plot_time_freq(t, fs, windowed_signal, FFT_size,"Windowed Noisy IQ")

#==============================================
# 3. AM modulation to simulate RPM changes in drone engines
#==============================================
am_signal = iq_gen.generate_quad_motor_am_signal(engine_rpm, blades, mod_index)
PlotUtils.plot_time_freq(t, fs, am_signal, FFT_size,"AM Modulated IQ")

noisy_am_signal = iq_gen.add_white_noise(am_signal, SNR_dB)
PlotUtils.plot_time_freq(t, fs, noisy_am_signal, FFT_size,"Noisy AM Modulated IQ")

#==============================================
# 4. Frequency hopping simulation
#==============================================

freq_hopped_signal = iq_gen.generate_fhss_signal(hopping_freqs, hop_duration)
PlotUtils.plot_time_freq(t, fs, freq_hopped_signal, FFT_size,"Frequency Hopped IQ")

noisy_fhss_signal = iq_gen.add_white_noise(freq_hopped_signal, SNR_dB)
PlotUtils.plot_time_freq(t, fs, noisy_fhss_signal, FFT_size,"Noisy Frequency Hopped IQ")

windowed_fhss_signal = iq_gen.apply_hanning_window(noisy_fhss_signal)
PlotUtils.plot_time_freq(t, fs, windowed_fhss_signal, FFT_size,"Windowed Noisy Frequency Hopped IQ")    

#==============================================
# 5. Superposition of signals
#==============================================
fhss = iq_gen.generate_fhss_signal(hopping_freqs, hop_duration)
fpv = iq_gen.generate_FPV_signal(video_bw_mhz, deviation_mhz)
m_doppler = iq_gen.generate_micro_doppler_signal(engine_rpm, blades, beta)
# Composite signal with different weights to simulate a more realistic scenario 
# where the drone signal is dominant but there are also FPV and motor Doppler components
composite_signal = fhss + (fpv * 0.5) + (m_doppler*0.8)

noisy_composite_signal = iq_gen.add_white_noise(composite_signal, SNR_dB)
windowed_composite_signal = iq_gen.apply_hanning_window(noisy_composite_signal)
PlotUtils.plot_time_freq(t, fs, windowed_composite_signal, FFT_size,"Full composite Drone Signal")
