//=========================================================================
// Processor <-> cache (packed bit vectors; cast to mem_*_t at DUT boundary)
//=========================================================================

`ifndef CACHE_PROC_IF_SV
`define CACHE_PROC_IF_SV

localparam int CACHE_PROC_REQ_W = 78;
localparam int CACHE_PROC_RSP_W = 48;

interface cache_proc_if ( input logic clk, input logic reset );
  logic [CACHE_PROC_REQ_W-1:0] req_msg;
  logic                        req_val;
  logic                        req_rdy;

  logic [CACHE_PROC_RSP_W-1:0] resp_msg;
  logic                        resp_val;
  logic                        resp_rdy;

  modport drv_mp (
    input  clk, reset, req_rdy, resp_val, resp_msg,
    output req_msg, req_val, resp_rdy
  );

  modport mon_mp (
    input clk, reset, req_msg, req_val, req_rdy, resp_msg, resp_val, resp_rdy
  );

endinterface

`endif
