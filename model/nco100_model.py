## NCO Phase Increment 
## phase increment = (f_out / f_clk) * 2^N
## N = 32: number of bits for phase accumulator
## Sin LUT (Q1.15): 16-bit signed integer, range [-32768, 32767]
## f_out = 30MHz because of undersampling (f_s = 70MHz, ADC: 100 MSPS)
## Phase accumulator : N = 32 bit



import numpy as np

N_LUT=256
OUT_WIDTH = 16
MAX_VAL = (2 ** (OUT_WIDTH - 1)) - 1 # 32767 for 16-bit signed integer
f_out = 30e6 # 30 MHz
f_clk = 100e6 # 100 MHz

#=================================================
# Phase Increment Calculation
#=================================================

phase_increment = int((f_out / f_clk) * (2**32))
print(f"Phase Increment: {phase_increment} ({phase_increment:032b})")

#=================================================
# Sin LUT generation
#=================================================
angles = np.linspace(0, np.pi/2, int(N_LUT/4)) # 0 to pi/2, 256/4 = 64 points
sin_lut = (MAX_VAL * np.sin(angles)).astype(int)
# np.sin(angles):[0,1], -> [0,32767] in signed integer

print("constant sin_lut : lut_type := (")
for i, val in enumerate(sin_lut):
    sep = "," if i < len(sin_lut) - 1 else ""
    val_bin = format (val, '016b')
    print(f"    {i:3d} => signed'(\"{val_bin}\"){sep}")
print(");") 





