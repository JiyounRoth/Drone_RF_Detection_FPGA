from scipy import signal
import numpy as np

class IQSignalGenerator:
    def __init__(self, fs, duration):
        self.fs = fs
        self.duration = duration
        self.t = np.arange(0, self.duration, 1/self.fs)
        self.fc = 70e6 # 70 MHz IF frequency

       
    def generate_tone(self, freq):
        t = self.t
        phase = 2 * np.pi * freq * t
        signal = np.exp(1j * phase)
        return t, signal
    
    # ==============================================
    # Add Gaussian noise to achieve SNR of 10 dB
    # SNR (dB) = 10 * log10(P_signal / P_noise)
    # ==============================================
    def add_white_noise(self, input_signal, snr_db = 10):
        
        signal_power = np.mean(np.abs(input_signal)**2)
        noise_power = signal_power / (10**(snr_db/10))
        if np.iscomplexobj(input_signal):
            noise_std = np.sqrt(noise_power / 2) # Divide by 2 for complex noise (I and Q components)  
            noise = np.random.normal(0, noise_std, input_signal.shape) + 1j*np.random.normal(0, noise_std, input_signal.shape)
        else:
            noise_std = np.sqrt(noise_power) # standard deviation of noise for real signals  
            noise = np.random.normal(0, noise_std, input_signal.shape)
        
        signal_with_noise = input_signal + noise
        return signal_with_noise


    # ==================================================================
    # AM modulation to simulate RPM changes in drone engines
    # ==================================================================  
    def am_modulated(self, input_signal,engine_rpm, blades, mod_index):
    
        # Convert RPM to Hz and multiply by number of blades for modulation frequency
        mod_freq = engine_rpm / 60 * blades 
        # The envelope is a real-valued scaling factor
        envelope = (1 + mod_index * np.sin(2 * np.pi * mod_freq * self.t)) 
        am_modulated_signal = input_signal * envelope
        # Complex (I+jQ) * Real (A) = (A*I + j*A*Q)
        return am_modulated_signal
    
    def generate_quad_motor_am_signal(self, engine_rpm, blades, mod_index):
        # Simulate 4 motors with slightly different RPMs to create a more complex signal
        _, base_carrier = self.generate_tone(self.fc)  # Base carrier at 70 MHz
        
        signals = []
        for i in range(4):
            rpm_variation = engine_rpm + np.random.uniform(-100, 100)  # Random variation of ±100 RPM
            motor_unit_signal = self.am_modulated(base_carrier, rpm_variation, blades, mod_index)
            signals.append(motor_unit_signal)
        
        # Combine signals from all motors (superposition)
        composite_am_signal = np.sum(signals, axis=0) / 4  # Normalize by number of motors
        return composite_am_signal
        
    # ==================================================================
    # FM modulation to simulate FPV, FHSS and Micro-Doppler effects
    # ==================================================================
    def generate_FPV_signal(self, video_bw_mhz=5.0, deviation_mhz=8.0):
        # Baseband random video content as Gaussian noise
        raw_video = np.random.normal(0, 1, len(self.t)) 
        # Analog LPF to limit bandwidth to 5 MHz, 
        sos = signal.butter(10, video_bw_mhz * 1e6, 'low', fs=self.fs, output='sos')        
        filtered_video = signal.sosfilt(sos, raw_video)
        
        # FM modulation Integral (kf * integral of video signal) 
        # Sensitivity factor (kf) determines the peak frequency
        kf = deviation_mhz * 1e6 
        phase_modulation = 2 * np.pi * kf * np.cumsum(filtered_video) / self.fs
        
        # Carrier Phase (Moves the signal to 70 MHz IF)
        carrier_phase = 2 * np.pi * self.fc * self.t
        
        # Final I/Q Signal: exp(j * (Carrier + Modulation))
        # Note: s(t) = exp(j * theta(t))
        FPV_iq_signal = np.exp(1j * (carrier_phase + phase_modulation))
        return FPV_iq_signal
       
    def generate_fhss_signal(self, hopping_freqs, hop_duration ):
        # hopping_freqs: centered around 70 MHz IF, within 30 MHz to 45 MHz range
        samples_per_hop = int(hop_duration * self.fs)
        
        # create a frequency array f[n] (Step function)
        f_n = np.repeat(hopping_freqs, samples_per_hop)
        
        if len(f_n) < len(self.t):
            # If f_n is shorter than t, it pads with the last frequency (hold last hop)
            f_n = np.pad(f_n, (0, len(self.t) - len(f_n)), mode='edge')
        else:
            f_n = f_n[:len(self.t)]  # Truncate to match the length of t
        
        
        # Phase Accumulation (Integral)
        # Phase_n = Sum of (2 * pi * f[n] / fs)
        phase_n = 2 * np.pi * np.cumsum(f_n) / self.fs
        # Generate the FHSS signal
        fhss_iq_signal = np.exp(1j * phase_n)
        return fhss_iq_signal



    def generate_micro_doppler_signal(self, engine_rpm, blades, beta): 
        # beta (0.01 to 0.2) controls the depth of modulation
        #  - stress test 0 01: 
        #  - realistic (small drone) 0.05
        #  - robust (large drone) 0.1 to 0.2

        t, carrier_signal = self.generate_tone(self.fc)
        
        # mechanical modulation frequency from blade rotation
        mod_freq = engine_rpm / 60 * blades  # Convert RPM to Hz
        # Phase deviation, real-valued oscillation added to the phase
        phase_wiggle = beta * np.sin(2 * np.pi * mod_freq * t)  
        # Combine: s(t) = exp(j * (2*pi*fc*t + phase_wiggle))
        micro_doppler_signal = carrier_signal * np.exp(1j * phase_wiggle)
        return micro_doppler_signal

   
