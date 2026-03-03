import numpy as np
import matplotlib.pyplot as plt

class PlotUtils:
    @staticmethod
    def plot_time_freq(t, fs, iq_signal, FFT_size,title):
        fig, axs = plt.subplots(1,2, figsize=(16,8))
        # Plot time domain (I and Q)
        axs[0].plot(t[:200]*1e6, np.real(iq_signal[:200]), label='I')
        axs[0].plot(t[:200]*1e6, np.imag(iq_signal[:200]), label='Q')
        axs[0].set_title(f"Time domain of {title} Signal (First 200 samples)")
        axs[0].set_xlabel("Time (µs)")
        axs[0].legend()
        axs[0].grid()
        
        # Plot frequency domain
        # fft for frequency domain analysis
        fft_iq_raw = np.fft.fft(iq_signal, n=FFT_size)
        freq_raw = np.fft.fftfreq(FFT_size, d=1/fs) #d:sampling interval
        # Shift zero frequency to center
        fft_iq_centered = np.fft.fftshift(fft_iq_raw)
        freq_centered = np.fft.fftshift(freq_raw)
        # Convert to Magnitude (dB)
        # Add small value to avoid log(0) and normalize by max magnitude for better visualization
        fft_iq_db = 20 * np.log10(np.abs(fft_iq_centered)/np.max(np.abs(fft_iq_centered)) + 1e-12)
        
        
        axs[1].plot(freq_centered/1e6, fft_iq_db, color ='orange', label='Magnitude (dB)')
        axs[1].set_title(f"Frequency domain of {title} Signal")
        axs[1].set_xlabel("Frequency (MHz)")
        axs[1].set_ylabel("Relative Magnitude (dB)")
        axs[1].set_xlim(-100, 5) # set range to see the noise floor
        axs[1].grid(True)
        plt.tight_layout()
        plt.show()
