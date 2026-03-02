# Drone_RF_Detection_FPGA
This project implements a high-performance RF Signal Detection pipeline on an FPGA specifically designed for Portabel/Handheld Counter-UAS (Unmanned Aircraft Systems) Hardware. The design focuses on real-time drone signal identification while minimizing power consumption and hardware resource footprints (SWaP optimization)

## 🚀 Key Features
- **Undersampling Strategy:** 100 MSPS sampling of 70 MHz IF (aliased to 30 MHz) to reduce FPGA computational load.
- **Micro-Doppler Extraction:** Models blade-induced phase/amplitude modulation (RPM-based signatures).
- **DSP Pipeline:** 2,048-point Radix-2 SDF FFT with 75% sliding overlap for transient FHSS capture.
- **Bit-True Modeling:** Python-based Golden Model for 16-bit fixed-point verification.

## 🛠 Tech Stack
- **Languages:** Python 3.12 (Modeling), VHDL-2008 (RTL)
- **Tools:** Xilinx Vivado (Artix-7/Zynq), GHDL, GTKWave, Cocotb
- **Hardware Target:** Xilinx Artix-7 (e.g., Basys3, Nexys Video) or Zynq-7000.

