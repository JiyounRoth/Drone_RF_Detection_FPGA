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

        fig, axs = plt.subplots(2,1, figsize = (10,10))
        
        
        axs[0].plot(shifted_freqs/1e6, np.abs(fft_sin), "b--", label = "sin")
        axs[0].plot(shifted_freqs/1e6, np.abs(fft_cos), "r--", label = "cos")
        axs[0].set_title(f"FFT of {filename} sin/cos")
        axs[0].set_xlabel("Frequency (MHz)")
        axs[0].set_ylabel("Normalized Magnitude")
        axs[0].grid()
        axs[0].legend()
        
                                        # add a tiny offset to prevent log10(0)
        axs[1].plot(shifted_freqs/1e6, 20*np.log10(np.abs(fft_sin)+ 1e-12), "b--", label = "sin [dB]") 
        axs[1].plot(shifted_freqs/1e6, 20*np.log10(np.abs(fft_cos)+ 1e-12), "r--", label = "cos [dB]")
        axs[1].set_title(f"FFT(dB) of {filename} sin/cos")
        axs[1].set_xlabel("Frequency (MHz)")
        axs[1].set_ylabel("Magnitude (dB)")
        axs[0].grid()
        axs[0].legend()
        
        fig.savefig(f"{filename}_sin_cos_fft.png")
        plt.close(fig)
    

    def plot_time_freq(fs,sin_vals, cos_vals, num_of_samples, filename):
        
        x_time= np.arange(num_of_samples)/fs
        PlotUtils.plot_time_domain(x_time,sin_vals, cos_vals, filename )
        PlotUtils.plot_fft(fs, sin_vals, cos_vals, filename)
