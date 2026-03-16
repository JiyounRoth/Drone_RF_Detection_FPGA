  GNU nano 7.2                                 Makefile
SIM = ghdl
TOPLEVEL_LANG = vhdl

VHDL_SOURCES = rtl/NCO100.vhd \
               rtl/nco_LUT.vhd
TOPLEVEL = nco100
COCOTB_TEST_MODULES = tb.test_nco100

GHDL_ARGS += --std=08
SIM_ARGS += --vcd=wave.vcd

include $(shell cocotb-config --makefiles)/Makefile.sim
