import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

class PlotUtils:
    @staticmethod
    def plot_time_domain(x_time, sin_vals, cos_vals, filename):
        
        plt.figure(figsize=(10,5))
        plt.plot(x_time, sin_vals,"bo", label="sin")
        plt.plot(x_time, cos_vals,"ro", label="cos")
        plt.title(f"{filename} sin/cos in timedomain")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.legend()
        plt.grid()
        plt.savefig(f"{filename}_sin_cos.png")
        plt.close()

    @staticmethod
    def plot_fft(fs, sin_vals, cos_vals, filename):

        N = len(sin_vals)
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
    

    def plot_time_freq(fs,sin_vals, cos_vals, num_of_samples, filename):
        
        x_time= np.arange(num_of_samples)/fs
        PlotUtils.plot_time_domain(x_time,sin_vals, cos_vals, filename )
        PlotUtils.plot_fft(fs, sin_vals, cos_vals, filename)
        
