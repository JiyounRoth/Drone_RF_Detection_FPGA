import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

class PlotUtils:
    @staticmethod
    def plot_time_freq(fs,sin_vals, cos_vals, num_of_samples, filename):
        
        N = num_of_samples
        x = np.arange(N)/fs

        plt.figure(figsize=(10,5))
        plt.plot(x, sin_vals,"bo", label="sin")
        plt.plot(x, cos_vals,"ro", label="cos")
        plt.title(f"{filename} sin/cos in timedomain")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.grid()
        plt.savefig(f"{filename}_sin_cos.png")
        plt.close()

        
        freqs = np.fft.fftfreq(N, d=1/fs)
        fft_sin = np.fft.fftshift(np.fft.fft(sin_vals)/N)
        fft_cos = np.fft.fftshift(np.fft.fft(cos_vals)/N)
        shifted_freqs = np.fft.fftshift(freqs)

        plt.figure(figsize=(10,5))
        plt.plot(shifted_freqs/1e6, np.abs(fft_sin), "b--", label = "sin")
        plt.plot(shifted_freqs/1e6, np.abs(fft_cos), "r--", label = "cos")
        plt.title(f"FFT of {filename} sin/cos")
        plt.xlabel("Frequency (MHz)")
        plt.ylabel("Normalized Magnitude")
        plt.grid()
        plt.legend()
        plt.savefig(f"{filename}_sin_cos_fft.png")
        plt.close()
    

    
