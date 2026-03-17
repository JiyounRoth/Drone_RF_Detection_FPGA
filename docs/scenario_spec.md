Project Scenario: Real-time Drone RF Detection System

This project implements a high-performance RF Signal Detection pipeline on an FPGA specifically designed for Portabel/Handheld Counter-UAS (Unmanned Aircraft Systems) Hardware. The design focuses on real-time drone signal identification while minimizing power consumption and hardware resource footprints (SWaP optimization)

1. Target Environment & Portable Hardware Specs

    - Application: Battery-powered handheld drone detectors (Man-portable systems).
    
    - Target Signal: Drone Uplink/Downlink signals (FHSS/OFDM) at a 70 MHz intermediate Frequency (IF)

    - Sampling Strategy: Undersampling (Bandpass Sampling) at 100 MSPS to shift the 70 MHz IF to a 30 MHz aliased frequency, reducing the computational load on the FPGA while maintaining signal integrity.
    
    - Signal Characteristics: includes AWGN (Additive White Gaussian Noise) and Micro-Doppler signatures (simulated frequency modulations caused by rotating drone blades) to test the detection sensitivity and identification accuracy.

2. FPGA DSP Pipeline Architecture
    
    The system is custom-coded in VHDL with a focus on low-power, low-latency, real-time throughput:
    
    - Front-End: 16-bit Fixed-point quantization and Haa/Hamming Windowing to minimized spectral leakage.
    
    - Core Processor: A custom-coded 2,048-point FFT engine (Radix- 2 SDF Architecture) for high-resolution frequency analysis.
    
    - Temporal Resolution: 75% Overlapping (512-sample sliding interval) to ensure the capture of transient, short-burst drone signals (FHSS).

    - Efficiency Features: Implementation of Clock Gating and minimized logic toggling to extend battery life in portable hardware deplyments.
    
    - Detection Logic: Power Spectrum Density (PSD) calculation and dynamic thresholding to trigger a "Drone Detected" flag.

3. Development Methodology

    - Phase 1 (Python): Modeling the RF environment, evaluating SNR vs. Power trade-offs, and generating Golden Test Vectors.

    - Phase 2 (VHDL/RTL): Direct RTL coding for precise hardware control, focusing on Timing Closure and Low-Power Synthesis (Target: Xilinx Artix-7 or Zynq-7000 series).

    - Phase 3 (System Validation): Bit-true verification by comparing RTL simulation results with the Python Golden Model.

4. Development Environment: 
    - Language: Python 3.12+ (Signal Prototyping & cocotb Verification)
    - Editor: Visual Studio Code (with TerosHDL extension)
    - HDL: VHDL-2008
    - Simulator: GHDL & GTKWave
    - Synthesis: Xilinx Vivado (Target: XCK26 Zynq UltraScale+ MPSoC) - migrated Artix-7/Zynq-7000, now used as part of a larger drone project.

5. System Specification
    - Target signal : 70 MHz IF(Intermediate Frequency)
    - Sampling Rate (fs) : 100 MSPS (undersampling mode)
    - Aliased Frequency : 30 MHz (100 - 70)
    - FFT Size : 2,048 Taps (Frequency Resolution: 48.8 kHz)
    - Quantisation bits : 16 bits
    - Sliding Interval: 512 Samples (75% Overlap)
    - Windowing: Hann/Hamming Window for spectral leakage reduction
7. Hardwares
    - FPGA/SoC : AMD Kria K26 SOM (mounted on a KV260 Vision Starter Kit $249 + $59 (Kria KV260 Basic Accessory Pack))
    - RF Front-End/Receiver : Ettu USRP B200mini-i 
    - Vision Sensor: Raspberry Pi Camera Modue V2 : RF logic detects a 2.4GHz signal, it triggers the Vision AI to visually track the target drone.
    - Analog Interface (70MHz IF Scenario): Mini-Circuits BPF-F70+(Bandpass Filter), because of the Undersampling Scenario, it clears all noise except the 70MHz band before it hits the ADC, preventing "Ghost Signals" from ruining 100MPSP aliasing strategy
      
8. Project Structure
    - README.md
    - model/
        - main.py
            - signal_gen.py
            - undersampling_test.py
            - fixed_point_ref.py
        - nco
    - rtl/
    - sim/
        - Mixer
        - Low-pass Filters
        - Baseband IQ
        - Sliding FFT
          

    - docs/

7. Mathematical Modeling of Drone Signals
    
    A. Gaussian noise
    - $SNR (dB) = 10 * log10  \left( \frac{P_{signal}} {P_{noise}} \right)$

    B. Incidental AM (Engine & Blade Modulation)
    - Description: Simulates amplitude fluctuations caused by the periodic rotation of drone propellers (Blade Flashing)
      $$s_{AM}(t) = A(t) \cdot \cos(2\pi f_c t)$$
        - $A(t) = (1 + m * sin(2 \pi \cdot f_m \cdot t))$ : Amplitude modulation
        
        - $f_c$ is the carrier frequency (IF frequency)
        - $f_m$: Modulation frequency corresponding to the motor RPM (e.g., $f_m = \frac{\text{RPM}}{60} \times N_{Blades} $)

        - $m$: Modulation index (0 to 1) representing the depth of the shadow/reflection caused by the blades
    
    C. Frequency Modulation (FM) Variants
    - Wideband FM(analog FPV Video)
        - Description: Simulates the analog video feed from a drone's camera
        - Modeling: A baseband message is passed through a 10th-order Butterworth LPF(Second-Order Sections) to limit the occupied bandwidth to ~5-8 MHz, reflecting real-world analog transmitter constraints
          $$s_{FPV}(t) = \cos\left( 2\pi f_c t + 2\pi k_f \int m_{lpf}(\tau) d\tau \right)$$
    
    - Frequency Hopping Spread Spectrum (FHSS-Control Signal)
        - Description: Mimics the RC (Remote Control) uplink signal where the carrier frequency "hops" across a wide band to avoid interference and detection.
        - Modeling: The carrier frequency is no longer a constant, but a time-dependent step function $f_h(t)$
          $$s_{FHSS}(t) = \cos\left( 2\pi \int f_h(\tau) d\tau + \phi_0\right )$$
            where $f_h(t)$ is the hopping frequency at time t.
        - Discrete-Time Representation (FPGA/Python Implementation)
        In the digital domain, the integral is replaced by a Recursive Phase Accumulator. This is the mathematical basis for DDS(Direct Digital Synthesis)
        The phase $\theta[n]$ at sample $n$ is calculated recursively to maintain phase continuity:

        $$\theta[n] = \left( \theta[n-1] + 2\pi \frac{f[n]}{f_s} \right) \pmod{2\pi}$$
        -  The final discrete-time signal $s[n]$ is generated using a lookup table or CORDIC algorithm:

        $$s[n] = \cos(\theta[n])$$
        - Detection Challenge: Require high temporal resolution (75% FFT Overlap) to capture transient bursts before the signal moves to a new channel.

    - Micro-Doppler Effects (Blade-Induced Phase Modulation)
        - Description: Fine-grained frequency shifts caused by the mechanical rotation of propeller blades. This serves as a unique spectral "fingerprint" for drone identification.
        - Propeller Physics: The modulation frequency $f_m$ is determined by the motor's RPM and the physical blade count:
            
            $$f_m = \frac{\text{RPM}}{60} \times N_{Blades} $$
        
        - Modeling: Added as a periodic phase deviation to the carrier: 
        
            $$\phi_{blade}(t) = \beta \sin(2\pi f_m t)$$
        
        - Purpose: Provides a unique "spectral signature" used to distinguish drones from birds or static interference



    


