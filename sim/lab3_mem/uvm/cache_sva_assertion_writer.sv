//=========================================================================
// SVA_ASSERTION_WRITER
// Protocol-level assertions bound to lab3_mem_CacheAlt top-level interfaces.
//=========================================================================
`ifndef CACHE_SVA_ASSERTION_WRITER_SV
`define CACHE_SVA_ASSERTION_WRITER_SV

`include "vc/mem-msgs.v"

module cache_sva_assertion_writer #(
  parameter int unsigned PROC_RSP_MAX_LAT = 200,
  parameter int unsigned MEM_RSP_MAX_LAT  = 200
)(
  input logic         clk,
  input logic         reset,
  input mem_req_4B_t  proc_req_msg,
  input logic         proc_req_val,
  input logic         proc_req_rdy,
  input mem_resp_4B_t proc_rsp_msg,
  input logic         proc_rsp_val,
  input logic         proc_rsp_rdy,
  input mem_req_16B_t mem_req_msg,
  input logic         mem_req_val,
  input logic         mem_req_rdy,
  input mem_resp_16B_t mem_rsp_msg,
  input logic          mem_rsp_val,
  input logic          mem_rsp_rdy
);

  function automatic logic is_legal_req_type(logic [3:0] t);
    return (t == `VC_MEM_REQ_MSG_TYPE_READ) ||
           (t == `VC_MEM_REQ_MSG_TYPE_WRITE) ||
           (t == `VC_MEM_REQ_MSG_TYPE_WRITE_INIT);
  endfunction

  function automatic logic is_legal_rsp_type(logic [3:0] t);
    return (t == `VC_MEM_RESP_MSG_TYPE_READ) ||
           (t == `VC_MEM_RESP_MSG_TYPE_WRITE) ||
           (t == `VC_MEM_RESP_MSG_TYPE_WRITE_INIT);
  endfunction

  // --------------------
  // Legal message types
  // --------------------
  a_proc_req_type_legal: assert property (
    @(posedge clk) disable iff (reset)
      (proc_req_val && proc_req_rdy) |-> is_legal_req_type(proc_req_msg.type_)
  ) else $error("[SVA_ASSERTION_WRITER] Illegal proc req type=%0d", proc_req_msg.type_);

  a_proc_rsp_type_legal: assert property (
    @(posedge clk) disable iff (reset)
      (proc_rsp_val && proc_rsp_rdy) |-> is_legal_rsp_type(proc_rsp_msg.type_)
  ) else $error("[SVA_ASSERTION_WRITER] Illegal proc rsp type=%0d", proc_rsp_msg.type_);

  a_mem_req_type_legal: assert property (
    @(posedge clk) disable iff (reset)
      (mem_req_val && mem_req_rdy) |-> is_legal_req_type(mem_req_msg.type_)
  ) else $error("[SVA_ASSERTION_WRITER] Illegal mem req type=%0d", mem_req_msg.type_);

  a_mem_rsp_type_legal: assert property (
    @(posedge clk) disable iff (reset)
      (mem_rsp_val && mem_rsp_rdy) |-> is_legal_rsp_type(mem_rsp_msg.type_)
  ) else $error("[SVA_ASSERTION_WRITER] Illegal mem rsp type=%0d", mem_rsp_msg.type_);

  // --------------------------------
  // Ready/valid hold semantics
  // --------------------------------
  a_proc_req_hold_until_accept: assert property (
    @(posedge clk) disable iff (reset)
      (proc_req_val && !proc_req_rdy) |=> (proc_req_val && $stable(proc_req_msg))
  ) else $error("[SVA_ASSERTION_WRITER] proc req changed while stalled");

  a_mem_req_hold_until_accept: assert property (
    @(posedge clk) disable iff (reset)
      (mem_req_val && !mem_req_rdy) |=> (mem_req_val && $stable(mem_req_msg))
  ) else $error("[SVA_ASSERTION_WRITER] mem req changed while stalled");

  a_proc_rsp_hold_until_accept: assert property (
    @(posedge clk) disable iff (reset)
      (proc_rsp_val && !proc_rsp_rdy) |=> (proc_rsp_val && $stable(proc_rsp_msg))
  ) else $error("[SVA_ASSERTION_WRITER] proc rsp changed while stalled");

  // --------------------------------
  // Bounded response latency checks
  // --------------------------------
  a_proc_req_gets_rsp_bounded: assert property (
    @(posedge clk) disable iff (reset)
      (proc_req_val && proc_req_rdy) |-> ##[1:PROC_RSP_MAX_LAT] proc_rsp_val
  ) else $error("[SVA_ASSERTION_WRITER] proc request timed out (> %0d cycles)", PROC_RSP_MAX_LAT);

  a_mem_read_gets_rsp_bounded: assert property (
    @(posedge clk) disable iff (reset)
      (mem_req_val && mem_req_rdy && (mem_req_msg.type_ == `VC_MEM_REQ_MSG_TYPE_READ))
      |-> ##[1:MEM_RSP_MAX_LAT] mem_rsp_val
  ) else $error("[SVA_ASSERTION_WRITER] mem read request timed out (> %0d cycles)", MEM_RSP_MAX_LAT);

  // Useful coverage to prove check activation
  c_proc_req_gets_rsp: cover property (
    @(posedge clk) disable iff (reset)
      (proc_req_val && proc_req_rdy) ##[1:PROC_RSP_MAX_LAT] (proc_rsp_val && proc_rsp_rdy)
  );

endmodule

bind lab3_mem_CacheAlt cache_sva_assertion_writer u_cache_sva_assertion_writer (
  .clk         (clk),
  .reset       (reset),
  .proc_req_msg(proc2cache_reqstream_msg),
  .proc_req_val(proc2cache_reqstream_val),
  .proc_req_rdy(proc2cache_reqstream_rdy),
  .proc_rsp_msg(proc2cache_respstream_msg),
  .proc_rsp_val(proc2cache_respstream_val),
  .proc_rsp_rdy(proc2cache_respstream_rdy),
  .mem_req_msg (cache2mem_reqstream_msg),
  .mem_req_val (cache2mem_reqstream_val),
  .mem_req_rdy (cache2mem_reqstream_rdy),
  .mem_rsp_msg (cache2mem_respstream_msg),
  .mem_rsp_val (cache2mem_respstream_val),
  .mem_rsp_rdy (cache2mem_respstream_rdy)
);

`endif
