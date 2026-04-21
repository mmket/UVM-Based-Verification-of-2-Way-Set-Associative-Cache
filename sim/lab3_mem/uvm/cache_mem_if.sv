//=========================================================================
// Cache <-> memory (packed bit vectors; cast at DUT boundary)
//=========================================================================

`ifndef CACHE_MEM_IF_SV
`define CACHE_MEM_IF_SV

localparam int CACHE_MEM_REQ_W = 176;
localparam int CACHE_MEM_RSP_W = 146;

interface cache_mem_if ( input logic clk, input logic reset );
  logic [CACHE_MEM_REQ_W-1:0] req_msg;
  logic                       req_val;
  logic                       req_rdy;

  logic [CACHE_MEM_RSP_W-1:0] resp_msg;
  logic                       resp_val;
  logic                       resp_rdy;

  modport drv_mp (
    input  clk, reset, req_msg, req_val, req_rdy, resp_rdy,
    output resp_msg, resp_val
  );

  modport mon_mp (
    input clk, reset, req_msg, req_val, req_rdy, resp_msg, resp_val, resp_rdy
  );

endinterface

`endif
