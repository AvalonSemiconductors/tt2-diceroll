`default_nettype none
`timescale 1ns/1ps

module tb (
	input CLK,
	input RST,
	input ROLL,
	output [7:0] LEDS
	);
	
	initial begin
		$dumpfile ("tb.vcd");
		$dumpvars (0, tb);
		#1;
	end
	
	wire [7:0] inputs = {ROLL, RST, CLK};
	wire [7:0] outputs;
	assign LEDS = outputs[7:0];
	
	tt2_tholin_diceroll tt2_tholin_diceroll (
		`ifdef GL_TEST
			.vccd1( 1'b1),
			.vssd1( 1'b0),
		`endif
		.io_in (inputs),
		.io_out (outputs)
	);
endmodule
