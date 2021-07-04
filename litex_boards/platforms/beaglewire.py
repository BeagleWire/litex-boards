#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2021 Omkar Bhilare <ombhilare999@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

# BeagleWire FPGA Cape:
# - Crowd Supply campaign: https://www.crowdsupply.com/qwerty-embedded-design/beaglewire
# - Docs: https://beaglewire.github.io/
# - Software Repo: https://github.com/BeagleWire/BeagleWire
# - Hardware Files: https://github.com/BeagleWire/beagle-wire

from litex.build.generic_platform import *
from litex.build.lattice import LatticePlatform
from litex.build.lattice.programmer import IceStormProgrammer

# IOs ----------------------------------------------------------------------------------------------

_io = [

    # Clk / Rst
    ("clk12", 0, Pins("61"), IOStandard("LVCMOS33")),

    # Leds
    ("user_led_0",    0, Pins("28"), IOStandard("LVCMOS33")),
    ("user_led_1",    1, Pins("29"), IOStandard("LVCMOS33")),
    ("user_led_2",    2, Pins("31"), IOStandard("LVCMOS33")),
    ("user_led_3",    3, Pins("32"), IOStandard("LVCMOS33")), 

    # Button
    ("user_btn_0",    0, Pins("25"), IOStandard("LVCMOS33")),
    ("user_btn_1",    1, Pins("26"), IOStandard("LVCMOS33")),

    # GPMC
     ("gpmc", 0,
        # GPMC_AD
        Subsignal("gpmc_ad_0", Pins("134"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_1", Pins("136"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_3", Pins("21"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_4", Pins("22"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_5", Pins("135"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_6", Pins("138"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_7", Pins("23"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_8", Pins("24"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_9", Pins("139"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_10", Pins("2"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_11", Pins("1"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_12", Pins("141"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_13", Pins("3"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_14", Pins("144"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_ad_15", Pins("143"), IOStandard("LVCMOS33")),
        # GPMC_Control
        Subsignal("gpmc_advn", Pins("19"),  IOStandard("LVCMOS33")),
        Subsignal("gpmc_csn1", Pins("137"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_clk",  Pins("142"), IOStandard("LVCMOS33")),
        Subsignal("gpmc_wein", Pins("18"),  IOStandard("LVCMOS33")),
        Subsignal("gpmc_oen",  Pins("20"),  IOStandard("LVCMOS33")),
    ),

    # SPIFlash
    ("spiflash", 0,
        Subsignal("miso", Pins("67"), IOStandard("LVCMOS33")),
        Subsignal("mosi", Pins("68"), IOStandard("LVCMOS33")),
        Subsignal("sck",  Pins("70"), IOStandard("LVCMOS33")),
        Subsignal("ss",   Pins("71"), IOStandard("LVCMOS33")),    
    ),

    #sdram
    ("sdram", 0,
        #SDRAM Address 
        Subsignal("sdram_addr_0", Pins("118"), IOStandard("LVCMOS33")),
        Subsignal("sdram_addr_1", Pins("117"), IOStandard("LVCMOS33")),
        Subsignal("sdram_addr_2", Pins("116"), IOStandard("LVCMOS33")),
        Subsignal("sdram_addr_3", Pins("101"), IOStandard("LVCMOS33")),
        Subsignal("sdram_addr_4", Pins("81"), IOStandard("LVCMOS33")),
        Subsignal("sdram_addr_5", Pins("83"), IOStandard("LVCMOS33")),
        Subsignal("sdram_addr_6", Pins("90"), IOStandard("LVCMOS33")),
        Subsignal("sdram_addr_7", Pins("91"), IOStandard("LVCMOS33")),
        Subsignal("sdram_addr_8", Pins("82"), IOStandard("LVCMOS33")),
        Subsignal("sdram_addr_9", Pins("84"), IOStandard("LVCMOS33")),
        Subsignal("sdram_addr_10", Pins("119"), IOStandard("LVCMOS33")),
        Subsignal("sdram_addr_11", Pins("85"), IOStandard("LVCMOS33")),
        Subsignal("sdram_addr_12", Pins("87"), IOStandard("LVCMOS33")),
        #SDRAM data 
        Subsignal("sdram_data_0", Pins("96"), IOStandard("LVCMOS33")),
        Subsignal("sdram_data_1", Pins("97"), IOStandard("LVCMOS33")),
        Subsignal("sdram_data_2", Pins("98"), IOStandard("LVCMOS33")),
        Subsignal("sdram_data_3", Pins("99"), IOStandard("LVCMOS33")),
        Subsignal("sdram_data_4", Pins("95"), IOStandard("LVCMOS33")),
        Subsignal("sdram_data_5", Pins("80"), IOStandard("LVCMOS33")),
        Subsignal("sdram_data_6", Pins("79"), IOStandard("LVCMOS33")),
        Subsignal("sdram_data_7", Pins("78"), IOStandard("LVCMOS33")),
        Subsignal("sdram_bank_0", Pins("121"), IOStandard("LVCMOS33")),
        Subsignal("sdram_bank_1", Pins("120"), IOStandard("LVCMOS33")),
        #SDRAM Control 
        Subsignal("sdram_clk", Pins("93"), IOStandard("LVCMOS33")),
        Subsignal("sdram_cke", Pins("88"), IOStandard("LVCMOS33")),
        Subsignal("sdram_we",  Pins("128"), IOStandard("LVCMOS33")),
        Subsignal("sdram_cs",  Pins("122"), IOStandard("LVCMOS33")),
        Subsignal("sdram_dqm", Pins("94"), IOStandard("LVCMOS33")),
        Subsignal("sdram_ras", Pins("124"), IOStandard("LVCMOS33")),
        Subsignal("sdram_cas", Pins("125"), IOStandard("LVCMOS33")),
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    ("PMOD1", "37  39  42  44  38  41  43  45"),
    ("PMOD2", "47  49  55  60  48  52  56  62"),
    ("PMOD3", "107 112 114 129 110 113 115 130"),
    ("PMOD4", "7   9   15  12  4   8   10  11")
]

# Platform -----------------------------------------------------------------------------------------

class Platform(LatticePlatform):
    default_clk_name   = "clk12"
    default_clk_period = 1e9/12e6

    def __init__(self, toolchain="icestorm"):
        LatticePlatform.__init__(self, "ice40-hx8k-tq144", _io, _connectors, toolchain=toolchain)

    def create_programmer(self):
        return IceStormProgrammer()

    def do_finalize(self, fragment):
        LatticePlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk12", loose=True), 1e9/12e6)