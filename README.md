## Drone RF Detection FPGA (RF Module)

## Overview
This repository contains the RF signal detection module of a larger drone project. It implements a real-time FPGA-based pipeline to detect drone RF signals in a low-cost, educational/experimental setting. The focus is learning RF detection algorithms.

## Tech Stack
- **Languages:** Python 3.12 (Modeling), VHDL-2008 (RTL)  
- **Tools:** Xilinx Vivado, GHDL, GTKWave, Cocotb  
- **Hardware Target:** AMD Kria K26 SOM  
- **RF Receiver:** Pluto SDR (considered for this project)

## Target Signals
This project focuses on the 2.4 GHz and 900 MHz bands, as they are commonly used for drone control.

