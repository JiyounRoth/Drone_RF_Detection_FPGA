import numpy as np

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge

from tb.fixedpoint import FixedPoint
from tb.tb_plot_utils import PlotUtils

@cocotb.test()
async def test_nco100(dut):

    cocotb.start_soon(Clock(dut.clk,10,units='ns').start())

    dut.phase_inc.value = 1288490188
    num_of_samples = 2048
    sin_vals = [0]*num_of_samples
    cos_vals = [0]*num_of_samples
    # 2 clk Reset
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)
    
    
    # 1 clk latency
    await RisingEdge(dut.clk) 
    
    for i in range (num_of_samples):
        
        sin_val = FixedPoint.q1_15_to_float(dut.sin_out.value.signed_integer)
        cos_val = FixedPoint.q1_15_to_float(dut.cos_out.value.signed_integer)
        dut._log.info(f"Sample = {i}, sin_val = {sin_val}, cos_val = {cos_val} ")            
        sin_vals[i] = sin_val
        cos_vals[i] = cos_val

        await RisingEdge(dut.clk)

            
    #Plot in time domain
    PlotUtils.plot_time_freq(100e6, sin_vals, cos_vals, num_of_samples, "nco100")
   