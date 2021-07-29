/////////////////////////////////////////////////////////////
//   Function of IP: Top module for Litex Core with GPMC to wishbone Wrapper
//   Author: Omkar Bhilare
//   Email: omkarbhilare45@gmail.com
/////////////////////////////////////////////////////////////

`default_nettype none

module top 
(   
    //Serial Terminal
    output reg serial_tx,
	input wire serial_rx,

    // Clock and Reset
    input  wire     clk100,
    input  wire user_btn_n,
	inout wire sdram_clock,
    output reg [3:0] user_led0,

    // SDRAM Signals
	output reg spiflash_cs_n,
	output reg spiflash_clk,
	output reg spiflash_mosi,
	input wire spiflash_miso,

    //GPMC Input
    inout  wire [15:0]  gpmc_ad,  //Data Multiplexed with Address
    input  wire       gpmc_advn,  //ADVN(L : ADDR)
    input  wire       gpmc_csn1,  //Chip Select(Low - On)
    input  wire       gpmc_wein,  //Low = write operation
    input  wire        gpmc_oen,  //Low = Read Operation
    input  wire        gpmc_clk,  //GPMC clock
    
    //SDRAM:
    output wire [12:0] sdram_a,
    inout  wire [7:0]  sdram_dq,
    output wire [1:0]  sdram_ba,

    output  wire sdram_cke,
    output  wire sdram_ras_n,
    output  wire sdram_cas_n,
    output  wire sdram_we_n,
    output  wire sdram_cs_n,
    output  wire sdram_dm,
);

// Parameters for Address and Data
parameter ADDR_WIDTH = 16;
parameter DATA_WIDTH = 16;

// Wishbone Interfacing Nets:
wire [ADDR_WIDTH-1:0]     wbm_address;  //Wishbone Address Bus
wire [DATA_WIDTH-1:0]    wbm_readdata;  //Wishbone Data Bus for Read Access
wire [DATA_WIDTH-1:0]   wbm_writedata;  //Wishbone Bus for Write Access

wire     wbm_cycle;      //Wishbone Bus Cycle in Progress 
wire     wbm_strobe;     //Wishbone Data Strobe
wire     wbm_write;      //Wishbone Write Access 
wire     wbm_ack;        //Wishbone Acknowledge Signal 
wire     reset;          //Reset Signal
assign reset = 1'b1;     //Active Low Signal

gpmc_to_wishbone # (
    .ADDR_WIDTH(ADDR_WIDTH),      // Macro for Address  
    .DATA_WIDTH(DATA_WIDTH),      // Macro for Data
    .TARGET("ICE40")              // Target("ICE40")   fpga prmitive
                                  // Target("GENERAL") verilog implementaion
) wb_controller (
    //System Clock and Reset
    .clk(clk100),                    //FPGA Clock
    .reset(reset),              //Master Reset for Wishbone Bus
    
    // GPMC INTERFACE 
    .gpmc_ad(gpmc_ad),            //Data Multiplexed with Address
    .gpmc_clk(gpmc_clk),          //GPMC clock
    .gpmc_advn(gpmc_advn),        //ADVN(L : ADDR)
    .gpmc_csn1(gpmc_csn1),        //Chip Select(Low - On)
    .gpmc_wein(gpmc_wein),        //Low = write operation
    .gpmc_oen(gpmc_oen),          //Low = Read Operation
    
    //Wishbone Interface Signals
    .wbm_address(wbm_address),     //Wishbone Address Bus for Read/Write Data
    .wbm_readdata(wbm_readdata),   //Wishbone ReadData (The data needs to send to BBB)
    .wbm_writedata(wbm_writedata), //Wishbone Bus for Write Access (The data from blocks)
    .wbm_write(wbm_write),       //Wishbone Write(High = Write)
    .wbm_strobe(wbm_strobe),     //Wishbone Data Strobe(Valid Data Transfer)
    .wbm_cycle(wbm_cycle),       //Wishbone Bus Cycle in Progress 
    .wbm_ack(wbm_ack)            //Wishbone Acknowledge Signal from Slave
);

// SDRAM is initialize at  SDRAM @0x40000000...
// Wishbone has 16 bit Address
// So creating a virtual address using offset of 0x4000_0000

wire [31:0] wbm_address_offset = 32'h40000000 + wbm_address;

beaglewire beaglewire_dut
(
    // Serial Terminal
	.serial_tx(serial_tx),
	.serial_rx(serial_rx),

    //Master Clock and reset
	.clk100(clk100),
	.user_btn_n(user_btn_n),
    .sdram_clock(sdram_clock),
    .user_led0(user_led0),

    //
	.spiflash_cs_n(spiflash_cs_n),
	.spiflash_clk(spiflash_clk),
	.spiflash_mosi(spiflash_mosi),
	.spiflash_miso(spiflash_miso),

    //Wishbone Port
	.wb_adr(wbm_address_offset),
	.wb_dat_w(wbm_writedata),
	.wb_dat_r(wbm_readdata),
	.wb_cyc(wbm_cycle),
	.wb_stb(wbm_strobe),
	.wb_ack(wbm_ack),
	.wb_we(wbm_write),
    .wb_sel(2'b00),
	.wb_cti(),
	.wb_bte(),
	.wb_err(),
	
    //SDRAM Port
	.sdram_a(sdram_a),
	.sdram_dq(sdram_dq),
	.sdram_we_n(sdram_we_n),
	.sdram_ras_n(sdram_ras_n),
	.sdram_cas_n(sdram_cas_n),
	.sdram_cs_n(sdram_cs_n),
	.sdram_cke(sdram_cke),
	.sdram_ba(sdram_ba),
	.sdram_dm(sdram_dm)
);

endmodule
