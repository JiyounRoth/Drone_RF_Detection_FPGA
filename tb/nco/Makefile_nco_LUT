SIM = ghdl
TOPLEVEL_LANG = vhdl

VHDL_SOURCES = rtl/nco_LUT.vhd
TOPLEVEL = nco_lut
COCOTB_TEST_MODULES = tb.test_nco_lut

GHDL_ARGS += --std=08
SIM_ARGS += --vcd=wave.vcd

include $(shell cocotb-config --makefiles)/Makefile.sim
