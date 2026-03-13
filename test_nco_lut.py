import matplotlib
matplotlib.use("Agg") # select non-GUI backend
import matplotlib.pyplot as plt
import numpy as np
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge

@cocotb.test()
async def test_nco_lut(dut):
    
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    dut.addr_sin.value = 0
    dut.addr_cos.value = 0

    addr_width = int(dut.ADDR_WIDTH.value)
    data_depth = 2**addr_width 

    sin_vals = [0]* data_depth
    cos_vals = [0]* data_depth

    await RisingEdge(dut.clk)
   
    read_latency_1clk = None
   
    for addr in range (data_depth + 1):
        
        if addr < data_depth:
            # Address for sin and cos 
            sin_addr = addr
            cos_addr = data_depth-1-addr
            
            # drive addr to DUT
            dut.addr_sin.value = sin_addr 
            dut.addr_cos.value = cos_addr 

            #dut._log.info(f"1st. if-loof, sin_addr={sin_addr}, cos_addr={cos_addr}")

        await RisingEdge(dut.clk)

        if read_latency_1clk is not None:
            # Read sin and cos from DUT
            sin_val = int(dut.sin_abs.value)
            cos_val = int(dut.cos_abs.value)

            assert 0 <= sin_val <= 2**15 - 1, "sin value is out of range"
            assert 0 <= cos_val <= 2**15 - 1, "cos value is out of range"

            sin_vals[addr-1] = sin_val
            cos_vals[addr-1] = cos_val
            #dut._log.info(f"2nd. if-loof, addr={addr-1}: sin_vals[{addr-1}]={sin_vals[addr-1]}, cos_vals[{addr-1}]={cos_vals[addr-1]}")

        read_latency_1clk = 1
    
        
    # Log
    for i in range (data_depth):
        dut._log.info(f"addr={i}: sin={sin_vals[i]}, cos={cos_vals[i]}")
       
    
    #Plot
    x = np.linspace(0, data_depth-1, data_depth)
    plt.plot(x, sin_vals, color= "blue", marker="o",label="sin" )
    plt.plot(x, cos_vals, color= "red", marker="o", label="cos")
    plt.legend()
    plt.grid()
    plt.savefig("nco_LUT.png") 

        
        