# Drone_RF_Detection_FPGA
This project implements a high-performance RF Signal Detection pipeline on an FPGA specifically designed for Portabel/Handheld Counter-UAS (Unmanned Aircraft Systems) Hardware. The design focuses on real-time drone signal identification while minimizing power consumption and hardware resource footprints (SWaP optimization)

## Key Features
- **Undersampling Strategy:** 100 MSPS sampling of 70 MHz IF (aliased to 30 MHz) to reduce FPGA computational load.
- **Micro-Doppler Extraction:** Models blade-induced phase/amplitude modulation (RPM-based signatures).
- **DSP Pipeline:** 2,048-point Radix-2 SDF FFT with 75% sliding overlap for transient FHSS capture.
- **Bit-True Modeling:** Python-based Golden Model for 16-bit fixed-point verification.

## Tech Stack
- **Languages:** Python 3.12 (Modeling), VHDL-2008 (RTL)
- **Tools:** Xilinx Vivado, GHDL, GTKWave, Cocotb
- **Hardware Target:** XCK26 Zynq UltraScale+ MPSoC) - migrated Artix-7/Zynq-7000, now used as part of a larger drone project.

## Project Structure
- **model/** : Python scripts for signal synthesis and Golden Model verification
- **rtl/** : VHDL source files for DSP pipeline and top-level design.
- **sim/** : Testbenches and cocotb verification environments.
- **docs/** : Technical specidications and mathematical derivations for drone signatures.

## Current Development Status: 
### **Phase 1 (Python Prototyping)**
currently validating the **Mathematical Models** for drone signatures:
- [x] **FHSS:** Phase-continuous hopping using Recursive Phase Accumulators.
- [x] **FPV Video:** 10th-order Butterworth filtered Wideband FM.
- [x] **Micro-Doppler:** Periodic AM/PM modulation based on Motor RPM & Blade count.
- [ ] **Next:** 16-bit Fixed-point quantization and DDC (Digital Down Conversion) logic.

### **Phase 2 (RTL Implementation)**
Following the validation of the Python Golden Model, the next phase focuses on hardware synthesis for the Xilinx Artix-7/Zynq target.
- [ ] **Digital Mixer & NCO (DDC):**
  - Implementing a 16-bit signed Digital Mixer to shift the 30 MHz aliased IF to Baseband.
  - Inferring Xilinx DSP48E1 slices for high-speed I/Q separation to maximize SWaP efficiency.


